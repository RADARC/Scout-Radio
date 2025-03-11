"""
get a python command line on USB serial port and synchronise files
for MicroPython and CircuitPython devices
"""

import sys
import os
import subprocess
import shutil
import serial
import pexpect
import pexpect.fdpexpect

def not_implemented():
    """ exit with error status indicating functionality not implemented """
    sys.exit("not implemented")

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

class TestBoard:
    """ Base class for MicroPython and CircuitPython scout radio boards """
    def __init__(self, target_mountpoint, fileops):
        self.m_files = []
        self.m_child = None
        self.m_ostype = None
        self.m_mountpoint = target_mountpoint
        self.m_fileops = fileops
        self.m_homedir = None
        self.m_verbose = True

        # set up by setfiles invocation
        self.m_target_homedir = ""

    def create_pexepect_child(self):
        """ stub method intentionally not implemented in base class """

        assert self # pylint wants self referenced

        not_implemented()

    def setfiles(self, homedir, targetfiles):
        """ configure the list of host python files to be run on target """
        self.m_homedir = homedir
        self.m_files = targetfiles
        self.m_target_homedir = os.path.join(self.m_mountpoint, os.path.basename(self.m_homedir))

    def sendrepl(self, cmd, expect_repl=True):
        """ send a command to MicroPython or CircuitPython repl """

        self.m_child.sendline(cmd)

        if not expect_repl:
            return b""

        # timeout long enough for download patch etc.
        self.m_child.expect(">>> ", timeout = 8)

        if "Traceback" in self.m_child.before.decode():
            #
            # dump the traceback from target
            #
            print(self.m_child.before.decode())

            #
            # force failure - we have a traceback from target.
            # Could use False here but hopefully what's below
            # is more descriptive of what's gone wrong.
            #
            assert "Traceback" not in self.m_child.before.decode()

        return self.m_child.before

    def copy_files_to_target(self):
        """ copy files specified in 'setfiles' method from host to target """

        assert self.m_mountpoint
        assert self.m_target_homedir

        for installitem in self.m_files:

            (source_fullpath, dst) = get_src_dst_from_item(installitem)

            if not os.path.exists(source_fullpath):
                sys.exit(f"Error: {source_fullpath} not found")

            #
            # deal with relative or absolute paths on target
            #
            if dst[0] == '/':
                target_fullpath = os.path.join(self.m_mountpoint, dst[1:])
            else:
                target_fullpath = os.path.join(self.m_target_homedir, dst)

            #
            # works if target_fullpath is either a file or directory
            #
            self.m_fileops.ensuredirs(os.path.dirname(target_fullpath))

            if self.m_verbose:
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

        if self.m_verbose:
            print()

    def copy_files_from_target(self):
        """ copy files specified in 'setfiles' method from target to host """

        assert self.m_mountpoint
        assert self.m_target_homedir

        for installitem in self.m_files:

            (source_fullpath, dst) = get_src_dst_from_item(installitem)

            #
            # deal with relative or absolute paths on target
            #
            if dst[0] == '/':
                target_fullpath = os.path.join(self.m_mountpoint, dst[1:])
            else:
                target_fullpath = os.path.join(self.m_target_homedir, dst)

            if self.m_verbose:
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

    def identify(self):
        """ print the scout radio os/python type """
        self.sendrepl("import sys")
        text = self.sendrepl("print(sys.implementation.name)")
        ostype = text.decode().strip().split("\r\n")[1]
        print(f"{ostype} board created")
        self.m_ostype = ostype

    def ostype(self):
        """
        return string describing the type of python running on target.
        return None if the board is not initialised.
        """
        return self.m_ostype

    def initialise(self, expect_repl=True):
        """ get the test board ready for use using the python repl
            on the (USB) serial port """
        self.create_pexepect_child()
        self.copy_files_to_target()

        # odd case for code.py
        if not expect_repl:
            return

        self.create_repl()
        self.sendrepl("import os")
        target_homedirname = os.path.basename(self.m_homedir)
        self.sendrepl(f"os.chdir(\"{target_homedirname}\")")

    def revsync(self):
        """ pull files from target board back to host """
        self.create_pexepect_child()
        self.copy_files_from_target()

    def create_repl(self):
        """ stub method intentionally not implemented in base class """

        assert self # pylint wants self referenced

        not_implemented()

    def reboot(self, expect_repl=True):
        """ restart the python interpreter on target by sending CTRL+D """

        # expect_repl deals with odd case probably for code.py autorun
        self.sendrepl("\x04\r\n\r\n", expect_repl=expect_repl)


#
# could factor these two FileOPs objects out into a separate file
# but something to be said for keeping everything in one place
#
class FileOPsCP:
    """ target file/directory operations collection for Circuit Python """

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

        shutil.copyfile(src, dst)


class FileOPsMP:
    """ target file/directory operations collection for MicroPython """

    def __init__(self, board):
        self.m_board = board
        self.m_rshell_fileop_timeout = 30

    def ensuresingledir(self, dirpath):
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
            self.ensuresingledir(tmp)

    def deltree(self, dst):
        """ rm -rf equivalent for Micro Python """

        self.m_board.sendrshellcmd(f"rm -r {dst}", timeout = self.m_rshell_fileop_timeout)

    def copytree(self, src, dst):
        """ cp -a equivalent for Micro Python """

        self.m_board.sendrshellcmd(f"cp -r {src} {dst}", timeout = self.m_rshell_fileop_timeout)

    def copyfile(self, src, dst):
        """ cp equivalent for single file for Micro Python """

        self.m_board.sendrshellcmd(f"cp {src} {dst}", timeout = self.m_rshell_fileop_timeout)

#
# Circuit Python board
#
class TestBoardCP(TestBoard):
    """ A CircuitPython scout radio test board """

    def __init__(self, serialport):
        """ Create a CircuitPython scout radio test board """
        self.m_ser = serial.Serial()
        self.m_ser.baudrate = 115200
        self.m_ser.port = serialport

        #
        # work out where the circuit python filesystem is mounted
        #
        mountpoint = None
        with open('/proc/mounts', 'r', encoding="utf-8") as mounts:
            for line in mounts.readlines():
                candidate_mp = line.strip().split()[1]
                if "CIRCUITPY" in candidate_mp:
                    mountpoint = candidate_mp
                    break

        if not mountpoint:
            sys.exit("Error: Circuit python filesystem mount not found")

        #
        # Set mountpoint and fileops object member variables in base class
        # by passing them to the base class constructor.
        #
        # pylint seems to prefer this.
        #
        super().__init__(mountpoint, FileOPsCP())

    def create_pexepect_child(self):
        """ create a pexpect child object for CircuitPython """
        try:
            self.m_ser.open()

        except serial.SerialException as excep:
            sys.exit(f"{excep}")

        self.m_child = pexpect.fdpexpect.fdspawn(self.m_ser, timeout=5)

    def sendrepl(self, cmd, expect_repl=True):
        """ send a command to CircuitPython repl """

        #
        # use base class implementation with CR/LF tacked on
        #
        return super().sendrepl(cmd + "\r\n", expect_repl)

    def create_repl(self):
        """ get the CircuitPython repl ready on the serial port """
        #
        # rattle return key
        #
        self.sendrepl("")


#
# Micro Python board
#
class TestBoardMP(TestBoard):
    """ A MicroPython scout radio test board """

    def __init__(self):
        """ Create a MicroPython scout radio test board """

        self.m_rshell_debug = False

        #
        # Set mountpoint and fileops object member variables in base class
        # by passing them to the base class constructor.
        #
        # pylint seems to prefer this.
        #
        super().__init__("/pyboard", FileOPsMP(self))

    def create_pexepect_child(self):
        """ create a pexpect child object for MicroPython """
        self.m_child = pexpect.spawn("rshell", timeout=1)
        self.m_child.expect("> ")
        if "No MicroPython boards connected" in self.m_child.before.decode():
            sys.exit("Error: rshell: No MicroPython boards connected")

    def sendrshellcmd(self, cmd, timeout = 10):
        """ send a command to rshell """

        if self.m_rshell_debug:
            print(f"sending {cmd}")
        self.m_child.sendline(cmd)

        # can take a while to copy files in rshell
        self.m_child.expect("> ", timeout)

        return self.m_child.before.decode()

    def create_repl(self):
        """ get the MicroPython repl ready on the serial port """
        #
        # we're assuming we're in rshell here...
        #
        self.m_child.sendline('repl pyboard')

        #
        # We do get a couple of instances of chevrons here.
        # Swallow them all so child.before remains consistent.
        #
        self.m_child.expect(">>> ")
        self.m_child.expect(">>> ")


def boarddetect_circuitpython_serial(serialport):
    """ Detect via USB serial port if a board is running circuit python """
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = serialport

    try:
        ser.open()

    except serial.SerialException as excep:
        print(f"{excep}")
        return False

    try:
        child = pexpect.fdpexpect.fdspawn(ser, timeout=0.5)
        child.sendline("import sys\r\n")
        child.expect(">>>")
        child.sendline("print(sys.implementation.name)\r\n")
        child.expect(">>>")

    except pexpect.exceptions.TIMEOUT:
        return False

    return "circuitpython" in child.before.decode()


def boarddetect_circuitpython_usb():
    """ Detect via lsusb command if a board is running circuit python """

    # lighter weight than boarddetect_circuitpython_serial
    proc = subprocess.run(["lsusb"], shell = True, check = True, stdout=subprocess.PIPE)

    #
    # may not be too robust
    #
    return "Adafruit" in proc.stdout.decode()

def circuitpython():
    """ returns True if running on circuit python """

    return boarddetect_circuitpython_usb()


# capitals keeps pylint happy
G_BOARD = None

def getboard( serialport="/dev/ttyACM0" ):
    """ return a singleton test board, instantiating it if required """
    global G_BOARD

    if os.path.exists(serialport):
        if not G_BOARD:
            if circuitpython():
                #
                # Create a CircuitPython board
                #
                G_BOARD = TestBoardCP(serialport)
            else:
                #
                # Create a MicroPython board
                #
                # TODO rshell/serial port interaction
                # rshell won't respect serial port passed here
                # so long as we only have one board it's not an issue.
                # Longer term perhaps we can look at ditching rshell
                # if we can work out how to copy files back and forth.
                #
                G_BOARD = TestBoardMP()

    if not G_BOARD:
        sys.exit("Error: board not found")

    return G_BOARD


if __name__ == "__main__":
    SERIALPORT = "/dev/ttyACM0"
    myboard = getboard(SERIALPORT)

    if not myboard:
        print("No MicroPython/CircuitPython test boards found")
    else:
        myboard.initialise()
        print(f"repl available on serial port {SERIALPORT}")
