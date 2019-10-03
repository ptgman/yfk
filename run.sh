#!/bin/bash

YFK_DIR=$(cd $(dirname $0); pwd)

source $HOME/yfkenv/venv/bin/activate
pip install --upgrade yfk/proj/dist/yfk-*.*.*-py3-none-any.whl

PY_SCRIPT=$YFK_DIR/run.py
python $PY_SCRIPT
deactivate
