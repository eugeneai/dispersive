#!/bin/bash
export LD_PRELOAD="libstdc++.so.6"
DN=$(dirname $BASH_SOURCE) 
python $DN/src/icc/icc_rake_app.py $*


