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
    mp=$(mount | grep $1 | awk '{print $3}')

    rw=""

    if [ -n "${mp}" ]; then
        rw=$(mount | grep $1 | awk '{print $6}')
    fi

    if $(echo ${rw} | grep -q rw); then
        echo ${mp}
    fi
}

await_mount()
{
    while [ "$(mountpoint $1)" = "" ]; do
        sleep 0.1
    done

    while [ ! -s $(mountpoint $1)/$2 ]; do
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

copyfile()
{
    SF=$1
    MP=$2

    while [ ! -d ${MP} ]; do
        echo "waiting for ${MP}..."
        sleep 0.1
    done

    cp $(thisdir)/${SF} ${MP}
}

nuke()
{
    echo "Plug in USB with bootsel pressed until this progam continues..."
    echo "Ignore any mount windows opening - or dismiss them"
    await_mount RPI-RP2 INDEX.HTM
    echo "Copying flashnuke...."

    copyfile ${NUKEFILE} $(mountpoint RPI-RP2)

    sleep 1

    echo "Waiting for mountpoint RPI-RP2..."
    await_mount RPI-RP2 INDEX.HTM
    echo "system wiped"
}
