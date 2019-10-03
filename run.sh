#!/bin/bash

source $HOME/yfkenv/venv/bin/activate

YFK_DIR=$(cd $(dirname $0); pwd)
PY_SCRIPT=$YFK_DIR/run.py

pip install --upgrade yfk/proj/dist/yfk-*.*.*-py3-none-any.whl

python $PY_SCRIPT
