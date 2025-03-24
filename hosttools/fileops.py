""" Micro and Circuit Python file operations collections """

import os
import shutil
import filecmp

# Use duck typing for FileOPsCP and FileOPsMP
class FileOPsCP:
    """ target file/directory operations collection for Circuit Python """

    def __init__(self, mountpoint, mainfile):
        """ useful to store mountpoint and auto run file in fileops """
        self.m_mountpoint = mountpoint
        self.m_auto_run_file = mainfile

    def ensuredirs(self, dirpath):
        """ mkdir -p equivalent for Circuit Python """

        assert self # pylint wants self referenced

        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    def deltree(self, dirpath):
        """ rm -rf equivalent for Circuit Python """

        assert self # pylint wants self referenced

        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)

    def copytree(self, src, dst):
        """ cp -a equivalent for Circuit Python """

        assert self # pylint wants self referenced

        shutil.copytree(src, dst)

    def copyfile(self, src, dst):
        """ cp equivalent for single file for Circuit Python """

        assert self  # pylint wants self referenced

        if os.path.exists(dst):
            if not filecmp.cmp(src, dst):
                shutil.copyfile(src, dst)
        else:
            shutil.copyfile(src, dst)


class FileOPsMP:
    """ target file/directory operations collection for MicroPython """

    def __init__(self, board, mountpoint, mainfile):
        """ useful to store mountpoint and auto run file in fileops """
        self.m_board = board
        self.m_rshell_fileop_timeout = 30
        self.m_mountpoint = mountpoint
        self.m_auto_run_file = mainfile

    def ensure_single_dir(self, dirpath):
        """ mkdir equivalent for Micro Python """
        response = self.m_board.sendrshellcmd(f"ls {dirpath}")

        if "Cannot access" in response:
            self.m_board.sendrshellcmd(f"mkdir {dirpath}")


    def ensuredirs(self, dirpath):
        """ mkdir -p equivalent for Micro Python """

        dirlist = dirpath.split(os.path.sep)

        # expect dirlist to be something like ['', 'pyboard', 'Display']

        assert dirlist[1] == "pyboard"

        tmp = "/pyboard"

        for dirname in dirlist[2:]:
            tmp = os.path.join(tmp, dirname)
            self.ensure_single_dir(tmp)


    def deltree(self, dst):
        """ rm -rf equivalent for Micro Python """

        self.m_board.sendrshellcmd(f"rm -r {dst}", timeout = self.m_rshell_fileop_timeout)


    def copytree(self, src, dst):
        """ cp -a equivalent for Micro Python """

        self.m_board.sendrshellcmd(f"cp -r {src} {dst}", timeout = self.m_rshell_fileop_timeout)


    def copyfile(self, src, dst):
        """ cp equivalent for single file for Micro Python """

        self.m_board.sendrshellcmd(f"cp {src} {dst}", timeout = self.m_rshell_fileop_timeout)
