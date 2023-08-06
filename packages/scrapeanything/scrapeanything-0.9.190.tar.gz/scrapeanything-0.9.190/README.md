# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

How to generate a PIP package?
https://packaging.python.org/en/latest/tutorials/packaging-projects/

change setup.cfg version
py -m build
py -m twine upload --skip-existing dist/*