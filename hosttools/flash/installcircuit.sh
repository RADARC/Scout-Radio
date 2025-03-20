#!/usr/bin/env sh

# helper shell script to install circuit python

mountpoint()
{
    mount | grep $1 | awk '{print $3}'
}

await_mount()
{
    while [ "$(mountpoint $1)" = "" ]; do
        sleep 0.1
    done
}

echo "waiting for mountpoint - plug in USB with bootsel pressed until this continues"
echo "BEWARE ALL FILES WILL BE DELETED ON THE MICROPYTHON BOARD"
echo "Ignore any mount windows opening - or dismiss them"
await_mount RPI-RP2
echo "Copying flashnuke...."
cp flash_nuke.uf2 $(mountpoint RPI-RP2)

echo "sleeping briefly...."
sleep 5

echo "waiting for mountpoint RPI-RP2"
await_mount RPI-RP2
echo "Copying circuit python...."
cp adafruit-circuitpython-raspberry_pi_pico-en_GB-9.2.4.uf2 $(mountpoint RPI-RP2)

echo "waiting for mountpoint CIRCUITPYTHON"
await_mount CIRCUITPY
echo "Copying circuit python....done"
