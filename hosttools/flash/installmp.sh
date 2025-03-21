#!/usr/bin/env sh

# bomb on error
set -e

# helper shell script to install micro python

IMAGE=RPI_PICO_W-20241129-v1.24.1.uf2

. $(dirname $0)/nuke.sh

#
# make sure source image exists
#
checkfile ${IMAGE}

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

install_os ${IMAGE}

echo "Waiting for system to install..."
while ! lsusb | grep -q "MicroPython Board"; do
    sleep 0.1
done
echo "Waiting for system to install...done"
