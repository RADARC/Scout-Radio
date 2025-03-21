#!/usr/bin/env sh

if ! hosttools/flash/installcircuit.sh; then
    echo "flash failed"
    exit 1
fi

export PYTHONPATH=$(pwd)/hosttools
cd software
python3 sysinstall.py

