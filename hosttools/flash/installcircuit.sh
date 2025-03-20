#!/usr/bin/env sh

# helper shell script to install circuit python

. ./nuke.sh

nuke

echo "Copying circuit python...."
cp adafruit-circuitpython-raspberry_pi_pico-en_GB-9.2.4.uf2 $(mountpoint RPI-RP2)

echo "waiting for mountpoint CIRCUITPYTHON"
await_mount CIRCUITPY
echo "Copying circuit python....done"
echo "Unplug and replug USB to start using your new system"
