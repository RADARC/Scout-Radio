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

nuke()
{
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
}
