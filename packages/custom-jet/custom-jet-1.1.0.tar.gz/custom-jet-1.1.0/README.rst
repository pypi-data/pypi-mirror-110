To test you can add the folder jet/ into your project

# Release new version
- edit jet/__init__.py version
- python setup.py sdist
- if twine not installed 'pip install twine'
- twine upload dist/*
