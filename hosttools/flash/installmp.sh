#!/usr/bin/env sh

# bomb on error
set -e

# helper shell script to install micro python

IMAGE=RPI_PICO_W-20241129-v1.24.1.uf2

. $(dirname $0)/nuke.sh

checkfile ${IMAGE}

nuke

#
# initial banner/health warning
# change this if new images are supported
#
if $(echo ${IMAGE} | grep -q PICO_W); then
    echo "USING PICO WIRELESS IMAGE, your board must be a PICO-W."
    echo "Please CTRL-C now if not."
    echo "Image to be installed: ${IMAGE}"
    echo
else
    echo "Unsupported image"
    exit 1
fi

nuke

echo "Copying micro python...."
   
cp $(thisdir)/${IMAGE} $(mountpoint RPI-RP2)

echo "Waiting for system to install..."
while ! lsusb | grep -q "MicroPython Board"; do
    sleep 0.1
done
echo "Waiting for system to install...done"

#
# not sure if this check is any good anyway
#
if lsusb | grep -q MicroPython; then
    echo "Unplug and replug USB to start using your new system"
else
    echo "Board not found, perhaps."
fi
