# bomb on error
set -e

NUKEFILE=flash_nuke.uf2

thisdir()
{
    thisdir=$(dirname $0)

    if [ -z "${thisdir}" ]; then
        thisdir="."
    fi

    echo ${thisdir}
}

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

checkfile()
{
    if [ ! -s $(thisdir)/$1 ]; then
        echo "$0: $(thisdir)/$1 not found"
        exit 1 
    fi
}

nuke_disclaimer()
{
    checkfile ${NUKEFILE}
    echo "BEWARE ALL FILES WILL BE DELETED ON THE MICROPYTHON BOARD"
    echo "CTRL-C now to exit"
}

nuke()
{
    echo "Plug in USB with bootsel pressed until this progam continues..."
    echo "Ignore any mount windows opening - or dismiss them"
    await_mount RPI-RP2
    echo "Copying flashnuke...."
    cp $(thisdir)/${NUKEFILE} $(mountpoint RPI-RP2)

    sleep 1

    echo "Waiting for mountpoint RPI-RP2..."
    await_mount RPI-RP2
    echo "system wiped"
}
