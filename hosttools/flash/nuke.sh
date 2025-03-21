# bomb on error
set -e

NUKEFILE=flash_nuke.uf2

mountpoint()
{
    #
    # get filesystem mount of directory specified, if it's there
    # otherwise empty string
    #
    mount | grep $1 | awk '{print $3}'
}

await_mount()
{
    mount_dir=$1
    expected_file=$2
    
    #
    # loop till we find expected mount dir mounted in our filesystem
    #
    MP=$(mountpoint ${mount_dir})

    while [ "${MP}" = "" ]; do
        sleep 0.1
        MP=$(mountpoint ${mount_dir})
    done

    #
    # now wait for specified expected file specified showing up in mountpoint
    #
    while [ ! -s "${MP}/${expected_file}" ]; do
        sleep 0.1
    done

    echo ${MP}
}

checkfile()
{
    if [ ! -s $(dirname $0)/$1 ]; then
        echo "$0: $(dirname $0)/$1 not found"
        exit 1 
    fi
}

copyfile()
{
    sourcefile=$1
    mount_dir=$2

    echo "Copying ${sourcefile} to ${mount_dir}..."
    cp $(dirname $0)/${sourcefile} ${mount_dir}

    # automated stuff will happen - wait for it
    sleep 1
}

await_install_mount()
{
    await_mount RPI-RP2 INDEX.HTM
}

install_os()
{
    image=$1

    checkfile ${NUKEFILE}
    echo "BEWARE ALL FILES WILL BE DELETED ON THE MICROPYTHON BOARD."
    echo "CTRL-C now to exit."
    echo
    echo "Plug in USB with bootsel pressed until this progam continues..."
    echo "Dismiss any mount windows opening if possible."

    copyfile ${NUKEFILE} $(await_install_mount)

    echo "Awaiting filesystem after system reset...."
    await_install_mount > /dev/null

    copyfile ${image} $(await_mount RPI-RP2 INDEX.HTM)
}
