#!/bin/bash
#
rm -fr dist/ build/
python setup.py sdist bdist_wheel

export TWINE_REPOSITORY_URL=https://upload.pypi.org/legacy/
export TWINE_USERNAME=mrx1203

## set password to keyring
# keyring set https://upload.pypi.org/legacy/ $TWINE_USERNAME

exec twine upload dist/*
