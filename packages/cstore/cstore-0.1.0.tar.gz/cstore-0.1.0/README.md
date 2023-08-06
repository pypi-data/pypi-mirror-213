# cstore
## A tools to store and recall useful commands, specifically created to assist forgetful individuals like myself

# First create a source distribution with:
python setup.py sdist

# Upload to Test PyPI and verify things look right:
twine upload -r testpypi dist/*

# Upload to PyPI:
twine upload dist/*
twine upload --skip-existing dist/*

# For a detailed list of all available setup.py commands, do:
python setup.py --help-commands

# Generating distribution archives
python3 -m pip install --upgrade build
python3 -m build
# Uploading the distribution archives
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
