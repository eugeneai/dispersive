#!/bin/bash
export LD_PRELOAD="libstdc++.so.6"
export PYTHONPATH=./:python2/lib:python2/lib/site-packages
DN=$(dirname $BASH_SOURCE)
#python -u $DN/debug.py $DN/src/icc/icc_xray_app.py $*
python -u $DN/src/icc/icc_xray_app.py $*


