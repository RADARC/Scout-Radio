#!/usr/bin/env sh

# helper shell script to install micro python

. ./nuke.sh

nuke

echo "Copying micro python...."
cp RPI_PICO_W-20241129-v1.24.1.uf2 $(mountpoint RPI-RP2)

echo "sleeping briefly...."
sleep 10

#
# not sure if this check is any good anyway
#
if lsusb | grep -q MicroPython; then
    echo "Unplug and replug USB to start using your new system"
    echo "All is well"
else
    echo "Board not found, perhaps."
fi
