#!/bin/bash
export LD_PRELOAD="libstdc++.so.6"
DN=$(dirname $BASH_SOURCE)
python -u $DN/debug.py $DN/src/icc/icc_xray_app.py $*


