## Motivation

[Sphinx](https://www.sphinx-doc.org/en/master/index.html) with [sphinx.ext.autodoc](https://www.sphinx-doc.org/en/master/usage/quickstart.html#autodoc) is a tool to auto create documentation as HTML, pdf or other formats from your python code and doc strings.

Unfortunately it's unintuitive and error prone.
It does not find the correct target for links or even worse, links to a wrong target.
The following example does not even produce a warning:

```python
def x() -> None:
	'''
	Wrong target
	'''
	pass

class A:

	def x(self, x: int) -> int:
		'''
		Whatever
		'''
		return x * 2

	def y(self, x: int) -> 'tuple[int, int]':
		'''
		Referencing :meth:`~A.x` works, referencing :meth:`x` links to the function instead of the method.
		Why is there even the distinction between :meth: and :func:?
		'''
		x = self.x(x)
		return (x, x)
```

But after carefully reading the [documentation](https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cross-referencing-python-objects) this behaviour is actually to be expected.
[Stackoverflow answers](https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cross-referencing-syntax) confirm that there is little difference between the different roles (unless the target starts with a dot).

If you change `` :meth:`x` `` to `` :data:`x` `` in the above example the markup changes but sphinx will still happily link the function `x` without giving a warning (even with `nitpicky = True`).

And there are more cases where sphinx does not behave as I would have expected:

- https://github.com/sphinx-doc/sphinx/issues/4961
- https://github.com/sphinx-doc/sphinx/issues/11434

My take away is:

- Always set [`nitpicky = True`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-nitpicky) in conf.py (which will require to maintain a list of [`nitpick_ignore`](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-nitpick_ignore)).
- Never ever use relative references in sphinx.
  Always specify the complete path.
  But that is cumbersome to type and difficult to maintain.
- You need an additional external tool to check your references.


## Features

This script searches all `.py` and `.rst` files in `src` and `docs/source` to

- warn you about invalid references (target not existing, ambiguous target, wrong role).
- convert all valid, relative references to absolute references while preserving the same label which is displayed in the HTML file.
- optionally warn if a target does not match the label (see `--check-labels`).


## Limitations

- This script does not to work around [issue 11434](https://github.com/sphinx-doc/sphinx/issues/11434).
  Although it's easy enough to find the definition where the link should point to
  it's not that easy to change the link back when the method is overridden later on.
  Because how should I know whether the overriding method or the overridden method is meant?
  I would need to keep track of the original references in an external file
  and somehow connect it to the py/rst files even when code and/or documentation is changed.
- If a [:paramref:](https://pypi.org/project/sphinx-paramlinks/) refers to a function or method with a ``**kw`` parameter I am simply assuming that a parameter of that name is valid.
  Although it's possible to annotate ``**kw`` parameters with [Unpack](https://typing-extensions.readthedocs.io/en/latest/#Unpack) (see [PEP 692](https://peps.python.org/pep-0692/))
  I am defining the [typed dict](https://docs.python.org/3/library/typing.html#typing.TypedDict) in a ``if typing.TYPE_CHECKING`` block for backward compatibility.
  Therefore this information is not available for this program because it inspects the imported module.


## Installation

You can install this script with

```bash
pipx install sphinx-link-fixer
```

but you don't need to install it.

You can just download [main.py](https://gitlab.com/erzo/sphinx-link-fixer/-/raw/master/src/sphinx_link_fixer/main.py) and run it, no dependencies required.


## License

This script is free software and licensed under the [BSD Zero Clause License](https://gitlab.com/erzo/sphinx-link-fixer/-/blob/master/LICENSE).
