#!/usr/bin/env sh

# helper shell script to install circuit python

# bomb on error
set -e

IMAGE=adafruit-circuitpython-raspberry_pi_pico-en_GB-9.2.4.uf2

. $(dirname $0)/nuke.sh

checkfile ${IMAGE}

nuke

echo "Copying circuit python...."
cp $(thisdir)/${IMAGE} $(mountpoint RPI-RP2)

echo "waiting for mountpoint CIRCUITPYTHON"
await_mount CIRCUITPY
echo "Copying circuit python....done"
echo "Unplug and replug USB to start using your new system"
