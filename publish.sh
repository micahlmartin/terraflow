#!/bin/bash

python setup.py sdist
python setup.py bdist_wheel --universal
python setup.py sdist bdist_wheel upload -r pypi
