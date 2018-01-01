#!/bin/bash

deactivate >> /dev/null 2>&1
rm -rf ./nerfball/../venv >> /dev/null 2>&1
virtualenv -p python3 venv
source venv/bin/activate
pip install -e .
ls -lrt ./venv/bin/python
nerf-virtualenv.sh ./venv/bin/python
export NERF_OS_POPEN=0
export NERF_OS_REMOVE=0
export NERF_SUBPROCESS_CALL=1
python setup.py test

