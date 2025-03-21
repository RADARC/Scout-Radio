#!/usr/bin/env sh

# rebuild scout radio system from scratch

#
# install circuit python
#
if ! hosttools/flash/installcircuit.sh; then
    echo "flash failed"
    exit 1
fi

#
# install all Scout Radio stuff
#
export PYTHONPATH=$(pwd)/hosttools
cd software
python3 sysinstall.py
