#!/bin/bash

source $HOME/yfkenv/venv/bin/activate

YFK_DIR=$(cd $(dirname $0); pwd)
PY_SCRIPT=$YFK_DIR/run.py

python $PY_SCRIPT
