#!/bin/bash
#export LD_PRELOAD="libstdc++.so.6"
#export PYTHONPATH=./:python2/lib:python2/lib/site-packages
DN=$(dirname $BASH_SOURCE)
#python -u $DN/debug.py $DN/src/icc/icc_xray_app.py $*
rpyc_classic.py -p 12211 2> err.log > stdout.log &
sleep 1s
python2 -u $DN/src/icc/icc_xray_app.py $*
killall rpyc_classic.py



