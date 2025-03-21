#!/usr/bin/env sh

# helper shell script to install circuit python

# bomb on error
set -e

IMAGE=adafruit-circuitpython-raspberry_pi_pico-en_GB-9.2.4.uf2

. $(dirname $0)/nuke.sh

install_os ${IMAGE}

#
# Wait for mount CIRCUITPY showing up with code.py in it
# to detect we're done.
#
echo "Waiting for CircuitPython system to install..."
await_mount CIRCUITPY code.py
echo "Waiting for CircuitPython system to install...done"
