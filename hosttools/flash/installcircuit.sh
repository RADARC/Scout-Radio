#!/usr/bin/env sh

# helper shell script to install circuit python

# bomb on error
set -e

IMAGE=adafruit-circuitpython-raspberry_pi_pico-en_GB-9.2.4.uf2

. $(dirname $0)/nuke.sh

#
# make sure source image exists
#
checkfile ${IMAGE}

install_os ${IMAGE}

get_mount CIRCUITPY code.py

echo "Copying circuit python....done"
echo "Unplug and replug USB to start using your new system"
