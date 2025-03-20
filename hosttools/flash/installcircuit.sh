#!/usr/bin/env bash

# helper shell script to install circuit python

mountpoint()
{
    mount | grep RPI-RP2 | awk '{print $3}'
}

await_mount()
{
    echo "waiting for mountpoint - plug in USB with bootsel pressed until this continues"
    echo "BEWARE ALL FILES WILL BE DELETED ON THE MICROPYTHON BOARD"
    while [ "$(mountpoint)" = "" ]; do
        sleep 0.1
    done
}

await_mount
echo "Copying flashnuke...."
cp flash_nuke.uf2 $(mountpoint)

echo "unplug and replug USB then any key to continue"
read -n1 cont

await_mount
echo "Copying circuit python...."
cp adafruit-circuitpython-raspberry_pi_pico-en_GB-9.2.4.uf2 $(mountpoint)
echo "Copying circuit python....done"
