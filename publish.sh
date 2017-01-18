#!/bin/bash

python setup.py sdist
python setup.py bdist_wheel --universal
python setup.py sdist bdist_wheel upload -r http://docker.es.ad.adp.com:8081/artifactory/api/pypi/pypi-local/
