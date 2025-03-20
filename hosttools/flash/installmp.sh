#!/usr/bin/env sh

# helper shell script to install micro python

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
