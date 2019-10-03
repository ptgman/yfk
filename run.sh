#!/bin/bash

source ~/yfkenv/venv/bin/activate

YFK_DIR=$(cd $(dirname $0); pwd)
PY_SCRIPT=$YFK_DIR/sample.py

python $PY_SCRIPT
