#!/usr/bin/env python3

'''
Convert all relative references to absolute references in .py and .rst files
as a workaround for https://github.com/sphinx-doc/sphinx/issues/4961

This assumes a project structure like this:
root
├── src
│   └── package
├── docs
│   └── source
│       └── conf.py
└── venv

In order to figure out the correct references this script tries to import and inspect the code
for which the documentation should be fixed. Therefore this script must be run in an environment
where this code is installed. If --in-venv is not passed thris script runs itself in venv.
If venv does not exist it is created.
'''

__version__ = '1.1.1'


import os
import sys
import argparse
import re
import importlib
import builtins
import inspect
import logging
import dataclasses
import enum
import typing
from collections.abc import Iterator, Callable, Sequence
from types import ModuleType

logger = logging.getLogger(__name__)

#https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cross-referencing-python-objects
ROLES_PY = {'mod', 'func', 'data', 'const', 'class', 'meth', 'attr', 'exc', 'obj', 'paramref'}
ROLES_MEMBER = {'meth', 'attr'}
ROLES_OBJECT = {'func', 'data', 'const', 'class', 'exc', 'obj'}
ROLES_MODULE = {'mod'}
ROLES_FUNC = {'func', 'meth'}
ROLES_IGNORED = {'ref', 'python'}
ROLES_PARAMREF = {'paramref'}

FIX_ROLES = {
	'True' : 'obj',
	'False' : 'obj',
	'None' : 'obj',
	'str' : 'class',  # even if it is used as a function like repr, sphinx won't find it as func
	'int' : 'class',
	'float' : 'class',
	'repr' : 'func',
	'format' : 'func',

	# these are not found because std lib is not annoted
	'textwrap.TextWrapper.break_long_words' : 'attr',
	'textwrap.TextWrapper.break_on_hyphens' : 'attr',

	# this is not found because in reality TypedDict is a function, not a class
	'typing.TypedDict' : 'class',
}

MAGIC_MEMBERS_TO_BE_IGNORED = {'__class__', '__base__'}


class InvalidReference(Exception):
	pass


class DefinitionType(enum.Enum):
	MOD = enum.auto()
	VAR = enum.auto()
	FUNC = enum.auto()
	CLASS = enum.auto()
	EXC = enum.auto()
	METH = enum.auto()
	ATTR = enum.auto()
	PARAM = enum.auto()

	def __eq__(self, other: object) -> bool:
		if self is other:
			return True
		if isinstance(other, str):
			role = other
			if self is DefinitionType.MOD:
				return role in ROLES_MODULE
			if self is DefinitionType.VAR:
				return role == 'data' or role == 'const' or role == 'obj'
			if self is DefinitionType.FUNC:
				return role == 'func'
			if self is DefinitionType.CLASS:
				return role == 'class'
			if self is DefinitionType.EXC:
				return role == 'exc'
			if self is DefinitionType.METH:
				return role == 'meth'
			if self is DefinitionType.ATTR:
				return role == 'attr' or role == 'const'
			if self is DefinitionType.PARAM:
				return role == 'paramref'
			assert False
		return NotImplemented

@dataclasses.dataclass
class Definition:
	indentation: int
	definition_type: DefinitionType
	name: str

class Reference:

	re_definitions = r'^(?P<indentation>[\t ]*)(?P<def>def|class) (?P<name>[A-Za-z0-9_]+)'
	re_reference = r':(?P<role>[^:]+):`(?P<ref>[^`<>]+?)( <(?P<explicittarget>[^`]+)>)?`'
	reo_pattern = re.compile(f'{re_definitions}|{re_reference}', re.MULTILINE)

	@classmethod
	def iter(cls, mod_name: 'str|None', text: str) -> 'Iterator[Reference]':
		nested_defs: 'list[Definition]' = [Definition(-1, DefinitionType.MOD, mod) for mod in mod_name.split('.')] if mod_name else []

		for m in cls.reo_pattern.finditer(text):
			definition = m.group('def')
			if not definition:
				yield cls(tuple(nested_defs), m)
			elif mod_name:
				indentation = len(typing.cast(str, m.group('indentation')))
				name = typing.cast(str, m.group('name'))

				while nested_defs and indentation <= nested_defs[-1].indentation:
					del nested_defs[-1]

				if definition == 'class':
					def_type = DefinitionType.CLASS
				elif nested_defs[-1].definition_type is DefinitionType.CLASS:
					def_type = DefinitionType.METH
				else:
					def_type = DefinitionType.FUNC

				nested_defs.append(Definition(indentation, def_type, name))


	def __init__(self, nested_defs: 'tuple[Definition, ...]', m: 're.Match[str]') -> None:
		tgt = m.group('explicittarget')
		if tgt:
			lbl = m.group('ref')
			assert lbl
		else:
			tgt = m.group('ref')
			assert tgt
			if tgt.startswith('~'):
				tgt = tgt[1:]
				lbl = tgt.rsplit('.', 1)[-1]
			else:
				lbl = tgt
		if tgt.startswith('.'):
			tgt = tgt[1:]

		role = m.group('role')
		assert role

		# I cannot distinguish whether this belongs to an attribute or to the class but I think that does not matter.
		# In case of a method there is one level more which I need to strip if this is not a :paramref:.
		self.nested_defs = nested_defs
		self.lbl: 'typing.Final[str]' = lbl
		self.tgt: 'typing.Final[str]' = tgt
		self.role: 'typing.Final[str]' = role

		self.i0: 'typing.Final[int]' = m.start()
		self.i1: 'typing.Final[int]' = m.end()

	def format(self, *, role: 'str|None' = None, tgt: 'str|None' = None, lbl: 'str|None' = None) -> str:
		if not role:
			role = self.role
		if not tgt:
			tgt = self.tgt
		if not lbl:
			lbl = self.lbl

		if lbl == tgt:
			return f":{role}:`{tgt}`"
		elif lbl == tgt.rsplit('.', 1)[-1]:
			assert '.' in tgt   # otherwise lbl would equal tgt and the last then block would have been executed instead
			return f":{role}:`~{tgt}`"
		else:
			return f":{role}:`{lbl} <{tgt}>`"


@dataclasses.dataclass
class Object:

	full_name: str
	definition_type: DefinitionType
	internal: bool

	#: None means this is equivalent to :attr:`full_name`. If this is a str it is *not* a full name, it must be searched for with :meth:`Main.search_for_definition`.
	documented_at: 'str|None'



class Main:

	EXTENSIONS = {'.py', '.rst'}

	RETURNCODE_OK = 0
	RETURNCODE_INVALID_REFERENCE = 1


	def main(self, root: str, *, check_labels: bool) -> int:
		self.check_labels = check_labels
		self.returncode = self.RETURNCODE_OK
		self.objects: 'dict[str, list[Object]]' = {}
		self.tried_modules: 'set[str|None]' = set()
		self.functions_with_kw: 'set[str]' = set()
		self.scan_project(root)
		self.scan_module(None, builtins, internal=False)
		path_venv = os.path.join(root, 'venv')
		if os.path.isdir(path_venv):
			self.python_exe = os.path.join(path_venv, 'bin', 'python')
		else:
			logger.warning(f"{path_venv!r} does not exist, I am falling back to {self.python_exe!r}")
			self.python_exe = 'python'

		for mod, fn in self.iter_files(root):
			self.fix_file(mod, fn)

		return self.returncode


	# ------- scan -------

	def scan_project(self, root: str) -> None:
		path_src = os.path.join(root, 'src')

		for pkg_name in os.listdir(path_src):
			pkg_path = os.path.join(path_src, pkg_name)
			if not os.path.isdir(pkg_path):
				continue

			self.add_object(Object(pkg_name, DefinitionType.MOD, internal=True, documented_at=None))
			self.scan_package(pkg_name, pkg_path)

	def scan_package(self, pkg_name: str, pkg_path: str) -> None:
		for fn in os.listdir(pkg_path):
			mod_path = os.path.join(pkg_path, fn)
			if not os.path.isfile(mod_path):
				continue
			if not fn.lower().endswith('.py'):
				continue
			mod_name = fn[:-3]
			if mod_name == '__init__':
				mod_name = pkg_name
			else:
				mod_name = pkg_name + '.' + mod_name

			self.add_object(Object(mod_name, DefinitionType.MOD, internal=True, documented_at=None))
			mod = importlib.import_module(mod_name)
			self.scan_module(mod_name, mod, internal=True)

	def scan_module(self, mod_name: 'str|None', mod: ModuleType, *, internal: bool) -> None:
		self.tried_modules.add(mod_name)
		ignore_imported = internal
		for member_name, member in inspect.getmembers(mod):
			if mod_name:
				member_name = mod_name + '.' + member_name

			if ignore_imported:
				module_where_member_has_been_defined = inspect.getmodule(member)
				if module_where_member_has_been_defined and module_where_member_has_been_defined != mod:
					continue
			if isinstance(member, ModuleType):
				continue

			if isinstance(member, BaseException):
				self.add_object(Object(member_name, DefinitionType.EXC, internal=internal, documented_at=None))
				self.scan_class(member_name, member, internal=internal)
			elif isinstance(member, type):
				self.add_object(Object(member_name, DefinitionType.CLASS, internal=internal, documented_at=None))
				self.scan_class(member_name, member, internal=internal)
			elif hasattr(member, '__call__'):
				self.add_object(Object(member_name, DefinitionType.FUNC, internal=internal, documented_at=None))
				self.scan_parameters(member_name, member, internal=internal)
			else:
				self.add_object(Object(member_name, DefinitionType.VAR, internal=internal, documented_at=None))

	def scan_class(self, cls_name: str, cls: 'type[typing.Any]|BaseException', *, internal: bool) -> None:
		for member_name, member in inspect.getmembers(cls):
			if member_name in MAGIC_MEMBERS_TO_BE_IGNORED:
				continue
			if cls is member:  # in python 3.6 there was a _gorg attribute which caused an infinite loop without this
				continue

			member_name = cls_name + '.' + member_name
			if isinstance(member, BaseException):
				self.add_object(Object(member_name, DefinitionType.EXC, internal=internal, documented_at=self.get_qual_name(member)))
				self.scan_class(member_name, member, internal=internal)
			elif isinstance(member, type):
				self.add_object(Object(member_name, DefinitionType.CLASS, internal=internal, documented_at=self.get_qual_name(member)))
				self.scan_class(member_name, member, internal=internal)
			elif hasattr(member, '__call__'):
				self.add_object(Object(member_name, DefinitionType.METH, internal=internal, documented_at=self.get_qual_name(member)))
				INIT = '.__init__'
				if member_name.endswith(INIT):
					member_name = member_name[:-len(INIT)]
				self.scan_parameters(member_name, member, internal=internal)
			else:
				self.add_object(Object(member_name, DefinitionType.ATTR, internal=internal, documented_at=self.get_qual_name(member)))

		self.add_annotated_attributes(cls_name, cls, internal=internal)

	def add_annotated_attributes(self, cls_name: str, cls: 'type[typing.Any]|BaseException', *, internal: bool) -> None:
		if hasattr(cls, '__annotations__'):
			for member_name, annotation in cls.__annotations__.items():
				if isinstance(annotation, str) and annotation.startswith('Callable['):
					deftype = DefinitionType.METH
				else:
					deftype = DefinitionType.ATTR
				qual_member_name = cls_name + '.' + member_name
				if not self.has_object(qual_member_name, deftype):
					self.add_object(Object(qual_member_name, deftype, internal=internal, documented_at=self.get_qual_name(cls, member_name)))

		for cls in getattr(cls, '__bases__', []):
			self.add_annotated_attributes(cls_name, cls, internal=internal)

	def scan_parameters(self, func_name: str, func: 'Callable[... , typing.Any]', *, internal: bool) -> None:
		try:
			signature = inspect.signature(func)
		except ValueError:
			return
		for param_name, param in signature.parameters.items():
			if param.kind is param.VAR_KEYWORD:
				self.functions_with_kw.add(func_name)
				continue
			qual_param_name = func_name + '.' + param_name
			self.add_object(Object(qual_param_name, DefinitionType.PARAM, internal=internal, documented_at=self.get_qual_name(func, param_name)))


	def get_qual_name(self, obj: object, name: 'str|None' = None) -> 'str|None':
		qualname = getattr(obj, '__qualname__', None)
		if not qualname:
			return None
		assert isinstance(qualname, str)
		if name:
			return qualname + '.' + name
		return qualname

	def add_object(self, obj: Object) -> None:
		short_name = obj.full_name.rsplit('.', 1)[-1]
		self.objects.setdefault(short_name, []).append(obj)

	def has_object(self, full_name: str, definition_type: 'DefinitionType|str') -> bool:
		short_name = full_name.rsplit('.', 1)[-1]
		for obj in self.objects.get(short_name, []):
			if obj.full_name == full_name and obj.definition_type == definition_type:
				return True
		return False


	# ------- fix references -------

	def fix_file(self, mod: 'str|None', fn: str) -> None:
		'''
		:param mod: The name of the module if :paramref:`fn` is a python module
		:param fn: The full name of the path to be fixed
		'''
		logging.info(f"========== {fn} ==========")
		is_py = os.path.splitext(fn)[1].lower() == '.py'
		fixes: 'list[tuple[Reference, str]]' = []
		with open(fn, 'rt') as f:
			content = f.read()
			for ref in Reference.iter(mod, content):
				self.check_label(fn, content, ref)
				if not self.is_valid(is_py, ref):
					fixes.append((ref, self.get_fix(fn, content, ref)))

		offset = 0
		for ref, repl in fixes:
			i0 = ref.i0 + offset
			i1 = ref.i1 + offset
			content = content[:i0] + repl + content[i1:]

			old_len = i1 - i0
			new_len = len(repl)
			offset += new_len - old_len

		with open(fn, 'wt') as f:
			f.write(content)

	def get_fix(self, fn: str, content: str, ref: Reference) -> str:
		if ref.tgt in FIX_ROLES:
			return ref.format(role=FIX_ROLES[ref.tgt])

		try:
			tgt = self.search_for_definition(ref)
		except InvalidReference as e:
			lnno = content[:ref.i0].count('\n') + 1
			logger.error(f"{e} Please fix this manually in {fn!r} line {lnno}.")
			self.returncode = self.RETURNCODE_INVALID_REFERENCE
			return ref.format()

		return ref.format(tgt=tgt)


	def search_for_definition(self, ref: Reference) -> str:
		if ref.role not in ROLES_PY:
			raise InvalidReference(f"Unknown role {ref.role!r}.")

		possible_targets = self.search_for_definitions(ref)

		if not possible_targets:
			for i in range(ref.tgt.count('.')):
				try:
					mod_name = ref.tgt.rsplit('.', i+1)[0]
					if mod_name in self.tried_modules:
						break
					self.tried_modules.add(mod_name)
					mod = importlib.import_module(mod_name)
					self.scan_module(mod_name, mod, internal=False)
					possible_targets = self.search_for_definitions(ref)
				except ImportError:
					pass

		if not possible_targets:
			raise InvalidReference(f"Failed to find a definition for {ref.role} {ref.tgt!r} in {'.'.join(d.name for d in ref.nested_defs)}.")
		if len(possible_targets) > 1:
			raise InvalidReference(f"{ref.role} {ref.tgt!r} in {'.'.join(d.name for d in ref.nested_defs)} is ambiguous, could be {', '.join(possible_targets)}.")
		return possible_targets[0]

	def search_for_definitions(self, ref: Reference) -> 'list[str]':
		if ref.role in ROLES_PARAMREF and '.' not in ref.tgt:
			if ref.nested_defs and ref.nested_defs[-1].definition_type is DefinitionType.METH and ref.nested_defs[-1].name == '__init__':
				i1 = -1
			else:
				i1 = None
			func_name = '.'.join(d.name for d in ref.nested_defs[:i1])
			tgt = func_name + '.' + ref.tgt
			if self.has_object(tgt, DefinitionType.PARAM):
				return [tgt]
			elif func_name in self.functions_with_kw:
				# I cannot check whether ref.tgt is valid or not, I'll leave that to sphinx
				return [tgt]
			else:
				return []
		elif ref.role in ROLES_PARAMREF and ref.tgt.count('.') == 1 and ref.nested_defs and ref.nested_defs[-1].definition_type is DefinitionType.METH:
			tgt = '.'.join(d.name for d in ref.nested_defs[:-1]) + '.' + ref.tgt
			if self.has_object(tgt, DefinitionType.PARAM):
				return [tgt]
			#else:
				# When referencing the parameter of a constructor from a different method
				# ref.tgt is 'ClassName.param' and ref.nested_defs is 'pkg.mod.ClassName.meth'
				# resulting in tgt = 'pkg.mod.ClassName.ClassName.param' which is invalid because the class is duplicated.
				# In this case the usual algorithm should be tried instead.
		elif ref.role in ROLES_PARAMREF:
			func_name, param_name = ref.tgt.rsplit('.', 1)
			if func_name in self.functions_with_kw:
				# I cannot check whether ref.tgt is valid or not, I'll leave that to sphinx
				return [ref.tgt]

		elif ref.role in ROLES_MEMBER and '.' not in ref.tgt and ref.nested_defs:
			if ref.nested_defs[-1].definition_type is DefinitionType.METH:
				i1 = -1
			else:
				i1 = None

			cls_name = '.'.join(d.name for d in ref.nested_defs[:i1])
			tgt = cls_name + '.' + ref.tgt
			if self.has_object(tgt, ref.role):
				return [tgt]
			else:
				return []

		possible_targets = []
		for obj in self.objects.get(ref.tgt.rsplit('.', 1)[-1], []):
			if not obj.internal:
				continue
			if ref.role != obj.definition_type:
				continue
			if ref.tgt == obj.full_name or obj.full_name.endswith('.' + ref.tgt):
				possible_targets.append(obj.full_name)

		if not possible_targets:
			for obj in self.objects.get(ref.tgt.rsplit('.', 1)[-1], []):
				if ref.role != obj.definition_type:
					continue
				if ref.tgt == obj.full_name or obj.full_name.endswith('.' + ref.tgt):
					possible_targets.append(obj.full_name)

		return possible_targets

	def is_valid(self, is_py: bool, ref: Reference) -> bool:
		if ref.role in ROLES_IGNORED:
			return True

		if ref.role in ROLES_MODULE:
			return self.is_installed_module(ref.tgt)
		if ref.tgt in FIX_ROLES and ref.role != FIX_ROLES[ref.tgt]:
			return False
		if is_py and ref.role in ROLES_MEMBER and '.' not in ref.tgt:
			return False

		return False

	re_name = '[A-Za-z_][A-Za-z0-9_]*'
	reo_lbl = re.compile(rf'(?P<name>({re_name}\.)*{re_name})')
	def check_label(self, fn: str, content: str, ref: Reference) -> None:
		if not self.check_labels:
			return

		if ref.role not in ROLES_PY:
			return

		m = self.reo_lbl.match(ref.lbl)
		if not m:
			return

		lbl = m.group('name')
		if not ref.tgt.endswith(lbl):
			lnno = content[:ref.i0].count('\n') + 1
			logger.warning(f"The label {lbl!r} is not the end of the target {ref.tgt!r} in {fn!r} line {lnno}.")
			self.returncode = self.RETURNCODE_INVALID_REFERENCE

	def is_installed_module(self, name: str) -> bool:
		try:
			importlib.import_module(name)
			return True
		except ImportError:
			return False


	# ------- select files -------

	def iter_files(self, root: str) -> 'Iterator[tuple[str|None, str]]':
		src = os.path.join(root, 'src')
		if not src.endswith(os.path.sep):
			src += os.path.sep
		len_src = len(src)
		for fn in self._iter_files(src):
			yield os.path.splitext(fn[len_src:])[0].replace(os.path.sep, '.'), fn
		for fn in self._iter_files(os.path.join(root, 'docs', 'source')):
			yield None, fn

	def _iter_files(self, directory: str) -> 'Iterator[str]':
		for name in os.listdir(directory):
			p = os.path.join(directory, name)
			if self.is_file_to_be_fixed(p):
				yield p
			elif os.path.isdir(p):
				yield from self._iter_files(p)

	def is_file_to_be_fixed(self, fn: str) -> bool:
		return os.path.isfile(fn) and os.path.splitext(fn)[1] in self.EXTENSIONS


class PrintVersion(argparse.Action):

	def __init__(self, option_strings: 'Sequence[str]', dest: str, **kwargs: typing.Any) -> None:
		kwargs.setdefault('nargs', 0)
		argparse.Action.__init__(self, option_strings, dest, **kwargs)

	def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: typing.Any, option_string: typing.Optional[str] = None) -> typing.NoReturn:
		print(__version__)
		sys.exit(0)


def main(argv: 'list[str]|None' = None) -> None:
	p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	p.add_argument('root', help="The root path of the project where the references should be fixed")
	p.add_argument('-v', '--version', action=PrintVersion, help="show the version and exit")
	p.add_argument('--check-labels', action='store_true', help="Print a warning if a target does not end on the label. This can be useful to find typos but there are real applications for it so this is not enabled by default.")
	p.add_argument('--in-venv', action='store_true', help="The program is executed in an environment where the project to be fixed is installed. If this is not given this program tries to run itself in a virtual environment called venv located in root.")
	args = p.parse_args(argv)
	if args.in_venv:
		logging.basicConfig(level=logging.INFO, format='[%(levelname)-8s] %(message)s')
		m = Main()
		returncode = m.main(args.root, check_labels=args.check_labels)
		exit(returncode)
	else:
		import subprocess
		import shlex
		root = os.path.abspath(args.root)
		path_venv = os.path.join(root, 'venv')
		python = os.path.join(path_venv, 'bin', 'python3')
		if not os.path.exists(python):
			print("venv does not exist, creating a new one")
			subprocess.run(['python3', '-m', 'venv', path_venv])
			subprocess.run([python, '-m', 'pip', 'install', '-e', root])
		cmd = [python, __file__, '--in-venv'] + sys.argv[1:]
		print("running %s" % shlex.join(cmd))
		completed_process = subprocess.run(cmd)
		exit(completed_process.returncode)

if __name__ == '__main__':
	main()
