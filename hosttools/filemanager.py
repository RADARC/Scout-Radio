""" manages testboard files """
import sys
import os

VERBOSE_INSTALL = True

def get_src_dst_from_item(item):
    """ helper method to determine src/dst paths from thing to be installed """
    #
    # If a single string is specified, this is both the
    # source and destination filename.
    #
    # If a tuple is specified, the first item is the source
    # and the second the destination.
    #
    if isinstance(item, str):
        src = dst = item
    else:
        (src, dst) = item

    return (src, dst)


class FileManager:
    """ manages testboard files """
    def __init__(self, file_operations, target_mountpoint):
        self.m_fileops = file_operations
        self.m_files = []
        self.m_target_homedir = None
        self.m_mountpoint = target_mountpoint


    def set_target_homedir(self, homedir):
        """ configure the target home directory for the component """
        self.m_target_homedir = os.path.join(self.m_mountpoint, os.path.basename(homedir))

    def setfiles(self, targetfiles):
        """ configure the list of host python files to be run on target """

        self.m_files = targetfiles

    def __get_target_fullpath(self, dest):
        """ helper for copy_files to/from target """
        #
        # deal with relative or absolute paths on target
        #
        if dest[0] == '/':
            tgt_fullpath = os.path.join(self.m_mountpoint, dest[1:])
        else:
            tgt_fullpath = os.path.join(self.m_target_homedir, dest)

        return tgt_fullpath


    def copy_files_to_target(self):
        """ copy files specified in 'setfiles' method from host to target """

        for installitem in self.m_files:
            #
            # We may have no files to copy, legitimately.
            # Only assert if we are going to install some.
            #
            assert self.m_mountpoint
            assert self.m_target_homedir

            (source_fullpath, dst) = get_src_dst_from_item(installitem)

            if not os.path.exists(source_fullpath):
                sys.exit(f"Error: {source_fullpath} not found")

            target_fullpath = self.__get_target_fullpath(dst)

            #
            # works if target_fullpath is either a file or directory
            #
            self.m_fileops.ensuredirs(os.path.dirname(target_fullpath))

            if VERBOSE_INSTALL:
                ftype = "dir" if os.path.isdir(source_fullpath) else "file"

                print(f"{ftype}: {source_fullpath} -> {target_fullpath}")

            if os.path.isdir(source_fullpath):
                #
                # copy in source directory tree first deleting any
                # on target
                #
                self.m_fileops.deltree(target_fullpath)

                self.m_fileops.copytree(source_fullpath, target_fullpath)
            else:
                #
                # copy on the single file
                #
                self.m_fileops.copyfile(source_fullpath, target_fullpath)

        if self.m_files and VERBOSE_INSTALL:
            print()


    def copy_files_from_target(self):
        """ copy files specified in 'setfiles' method from target to host """

        # this method is used by install.py --revsync option

        assert self.m_mountpoint
        assert self.m_target_homedir

        for installitem in self.m_files:

            (source_fullpath, dst) = get_src_dst_from_item(installitem)

            target_fullpath = self.__get_target_fullpath(dst)

            if VERBOSE_INSTALL:
                ftype = "dir" if os.path.isdir(source_fullpath) else "file"

                print(f"{ftype}: {target_fullpath} -> {source_fullpath}")

            if os.path.isdir(source_fullpath):
                #
                # a bit dangerous
                #
                self.m_fileops.deltree(source_fullpath)

                self.m_fileops.copytree(target_fullpath, source_fullpath)
            else:
                #
                # copy off the single file
                #
                self.m_fileops.copyfile(target_fullpath, source_fullpath)
