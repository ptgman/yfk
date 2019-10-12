#!/bin/bash

source $HOME/yfkenv/venv/bin/activate
YFK_DIR=$(cd $(dirname $0); pwd)

python $YFK_DIR/monterm.py $@


deactivate
