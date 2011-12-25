#!/bin/bash
export LD_PRELOAD="libstdc++.so.6"
python src/icc/icc_xray_app.py $*


