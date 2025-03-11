"""
get a python command line on USB serial port and synchronise files
for MicroPython and CircuitPython devices
"""

import sys
import os
import subprocess
import argparse
import shutil
import serial
import pexpect
import pexpect.fdpexpect

def not_implemented():
    """ exit with error status indicating functionality not implemented """
    sys.exit("not implemented")


class TestBoard:
    """ Base class for MicroPython and CircuitPython scout radio boards """
    def __init__(self, target_mountpoint, fileops):
        self.m_files = []
        self.m_child = None
        self.m_ostype = None
        self.m_mountpoint = target_mountpoint
        self.m_fileops = fileops
        self.m_homedir = None

    def create_pexepect_child(self):
        """ stub method intentionally not implemented in base class """

        assert self # pylint wants self referenced

        not_implemented()

    def setfiles(self, homedir, targetfiles):
        """ configure the list of host python files to be run on target """
        self.m_homedir = homedir
        self.m_files = targetfiles

    def sendrepl(self, cmd):
        """ send a command to MicroPython or CircuitPython repl """

        self.m_child.sendline(cmd)

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

        if self.m_files:
            for item in self.m_files:
                if isinstance(item, str):
                    src = item
                    dst = item
                else:
                    (src, dst) = item

                source_fullpath = src

                if not os.path.exists(source_fullpath):
                    sys.exit(f"Error: {source_fullpath} not found")

                target_homedir = os.path.join(self.m_mountpoint, os.path.basename(self.m_homedir))

                self.m_fileops.ensuredir(target_homedir)

                if dst[0] == '/':
                    target_fullpath = os.path.join(self.m_mountpoint, dst[1:])
                else:
                    target_fullpath = os.path.join(target_homedir, dst)

                #
                # If we are installing a file, make sure its
                # destination directory exists on target.
                #
                if not os.path.isdir(source_fullpath):
                    self.m_fileops.ensuredir(os.path.dirname(target_fullpath))

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

    def copy_files_from_target(self):
        """ stub method intentionally not implemented in base class """

        assert self # pylint wants self referenced

        not_implemented()

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

    def initialise(self):
        """ get the test board ready for use using the python repl
            on the (USB) serial port """
        self.create_pexepect_child()
        self.copy_files_to_target()
        self.create_repl()
        self.sendrepl("import os")
        target_homedir = os.path.basename(self.m_homedir)
        self.sendrepl(f"os.chdir(\"{target_homedir}\")")

    def create_repl(self):
        """ stub method intentionally not implemented in base class """

        assert self # pylint wants self referenced

        not_implemented()

    def reboot(self):
        """ restart the python interpreter on target by sending CTRL+D """
        self.sendrepl("\x04\r\n\r\n")


class FileOPsCP:
    """ target file/directory operations collection for Circuit Python """

    def ensuredir(self, dirpath):
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

    def sendrepl(self, cmd):
        """ send a command to CircuitPython repl """

        #
        # use base class implementation with CR/LF tacked on
        #
        return super().sendrepl(cmd + "\r\n")

    def copy_files_from_target(self):
        """ copy files specified in 'setfiles' method from target to host """

        assert self.m_mountpoint

        for targetfile in self.m_files:
            target_fullpath = os.path.join(self.m_mountpoint, targetfile)
            host_fullpath = os.path.join(os.getcwd(), targetfile)

            shutil.copyfile(target_fullpath, host_fullpath)

    def create_repl(self):
        """ get the CircuitPython repl ready on the serial port """
        #
        # rattle return key
        #
        self.sendrepl("")

class FileOPsMP:
    """ target file/directory operations collection for MicroPython """

    def __init__(self, board):
        self.m_board = board
        self.m_rshell_fileop_timeout = 30

    def ensuredir(self, dirpath):
        """ mkdir -p equivalent for Micro Python """
        response = self.m_board.sendrshellcmd(f"ls {dirpath}")

        if "Cannot access" in response:
            self.m_board.sendrshellcmd(f"mkdir {dirpath}")

    def deltree(self, dst):
        """ rm -rf equivalent for Micro Python """

        self.m_board.sendrshellcmd(f"rm -r {dst}", timeout = self.m_rshell_fileop_timeout)

    def copytree(self, src, dst):
        """ cp -a equivalent for Micro Python """

        self.m_board.sendrshellcmd(f"cp -r {src} {dst}", timeout = self.m_rshell_fileop_timeout)

    def copyfile(self, src, dst):
        """ cp equivalent for single file for Micro Python """

        self.m_board.sendrshellcmd(f"cp {src} {dst}", timeout = self.m_rshell_fileop_timeout)


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

    def copy_files_from_target(self):
        """ copy files specified in 'setfiles' method from target to host """

        # exit may be a bit harsh here...but probably fair
        not_implemented()

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
    board = getboard(SERIALPORT)

    if not board:
        print("No MicroPython/CircuitPython test boards found")
    else:
        board.initialise()
        print(f"repl available on serial port {SERIALPORT}")

        parser = argparse.ArgumentParser()
        parser.add_argument("--revsync",
                            help="reverse sync: copy files from target to host",
                            action="store_true")
        args = parser.parse_args()
        if args.revsync:
            #
            # hacky...circular dependency between test.py and
            # testboard.py but very limited use here.
            #
            from test import TARGETFILES
            board.setfiles(TARGETFILES)
            board.copy_files_from_target()
