"""
get a python command line on USB serial port and synchronise files
for MicroPython and CircuitPython devices
"""

import sys
import os
import tempfile
import serial
import pexpect
import pexpect.fdpexpect
import fileops
import sysdetect

#
# beginnings of proper logging
#
VERBOSE_INSTALL = True
VERBOSE_SEND_REPL = False
VERBOSE_SEND_REPL_RESPONSE = False
VERBOSE_SEND_RSHELL = False
VERBOSE_SEND_RSHELL_RESPONSE = False

#
# handy formatter
#
def formatoutput(output):
    """ format output from target board """
    for line in output.split("\r\n"):
        print(line)


def not_implemented(unused):
    """ exit with error status indicating functionality not implemented """

    assert unused # pylint

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
    def __init__(self, serialport, target_mountpoint, file_operations, mainfile):
        self.m_files = []
        self.m_child = None
        self.m_ostype = None
        self.m_mountpoint = target_mountpoint
        self.m_fileops = file_operations
        self.m_auto_run_file = mainfile

        # set up by sethomedir invocation
        self.m_homedir = None
        self.m_target_homedir = None

        #
        # serial port scaffold stuff
        #
        self.m_ser = None
        self.m_serialportname = serialport

        #
        # record whether we have been initialised
        #
        self.m_initialised = False

    def serialportname(self):
        """ return serial port name """

        return self.m_serialportname

    def open_serial(self):
        """ open the serial device if necessary """

        if not self.m_ser:
            self.m_ser = serial.Serial()
            self.m_ser.baudrate = 115200
            self.m_ser.port = self.m_serialportname

            try:
                self.m_ser.open()

            except serial.SerialException as excep:
                sys.exit(f"{excep}")

        self.m_ser.reset_input_buffer()


    def close_serial(self):
        """ close the serial device """
        self.m_ser.close()
        self.m_ser = None

    def create_pexpect_child(self, send_cr=True):
        """ create a pexpect child object with python repl """

        self.open_serial()

        self.m_child = pexpect.fdpexpect.fdspawn(self.m_ser, timeout=5)

        if send_cr:
            # can't use sendrepl here as that potentially switches session type
            self.m_child.sendline("\r\n")


    def sethomedir(self, homedir):
        """ configure the home directory for the component """
        self.m_homedir = homedir
        self.m_target_homedir = os.path.join(self.m_mountpoint, os.path.basename(self.m_homedir))


    def setfiles(self, targetfiles):
        """ configure the list of host python files to be run on target """
        self.m_files = targetfiles

    def sendrepl(self, cmd, expect_repl=True):
        """ code not used, here just for pylint """

        # keep pylint from grumping
        assert self
        assert cmd
        assert expect_repl

        # should not be called
        assert False

        # pylint, can't get here anyway
        return ""


    def sendreplbase(self, cmd, expect_repl=True):
        """
            Base class code to send a command to MicroPython
            or CircuitPython repl. Tweaks to the invocation/behaviour
            are in the derived classes in sendrepl.

            Not to be used directly, generally.
        """

        if VERBOSE_SEND_REPL:
            print(f">>> {cmd}")

        self.m_child.sendline(cmd)

        # don't expect repl to come back to us - eg. autorun code.py
        if not expect_repl:
            return b""

        # timeout long enough for download patch etc.
        self.m_child.expect(">>> ", timeout = 8)

        output = self.m_child.before.decode()

        if VERBOSE_SEND_REPL_RESPONSE:
            print(output)

        if "Traceback" in output and not "KeyboardInterrupt:" in output:
            #
            # dump the traceback from target
            #
            print(output)

            #
            # force failure - we have a traceback from target.
            # Could use False here but hopefully what's below
            # is more descriptive of what's gone wrong.
            #
            assert "Traceback" not in output

        #
        # Don't echo the command sent.
        # Return the second line of output onwards.
        # The strip is debatable.
        #
        return "\r\n".join(output.split("\r\n")[1:]).strip()


    def get_target_fullpath(self, dest):
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

            target_fullpath = self.get_target_fullpath(dst)

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

            target_fullpath = self.get_target_fullpath(dst)

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


    def identify(self):
        """ print the scout radio os/python type """
        self.sendrepl("import sys")
        ostype = self.sendrepl("print(sys.implementation.name)")
        print(f"{ostype} board created")
        self.m_ostype = ostype


    def ostype(self):
        """
        return string describing the type of python running on target.
        return None if the board is not initialised.
        """
        return self.m_ostype


    def get_control(self):
        """
        send control c to target if unresponsive
        """

        #
        # TODO/latent BUG.
        # Not sure why we can't just unconditionally
        # throw a control-c at target eg. even if it
        # doesn't need interrupting i.e. is at the
        # usual python repl prompt >>>.
        #
        # If we do, "python testboard.py" with a board
        # present fails the board.identify() invocation.
        #
        # Aside: If the target is unresponsive due to code.py
        # or main.py autorun thing in place, testboard.py
        # can't cope with this anyway as it reboots the
        # board.
        #
        # Timeout used below is totally arbitrary to
        # determine whether the prompt is there or not.
        #
        try:
            self.m_child.expect(">>> ", timeout = 0.1)

        except pexpect.exceptions.TIMEOUT:
            self.ctrlc()


    def initialise(self, expect_repl=True):
        """ get the test board ready for use using the python repl
            on the (USB) serial port """
        self.create_pexpect_child()
        self.get_control()
        self.reboot()
        self.copy_files_to_target()

        #
        # a bit arbitrary
        #
        self.m_initialised = True

        # odd case for code.py
        if not expect_repl:
            return

        # homedir may necessarily not be set: eg. python testboard.py
        if self.m_homedir:
            self.sendrepl("import os")
            target_homedirname = os.path.basename(self.m_homedir)
            self.sendrepl(f"os.chdir(\"/{target_homedirname}\")")


    def initialised(self):
        """ return whether we have been initialised """

        return self.m_initialised


    def revsync(self):
        """ pull files from target board back to host """

        if self.m_files:
            self.create_pexpect_child()
            self.copy_files_from_target()


    def reboot(self, expect_repl=True):
        """ restart the python interpreter on target by sending CTRL+D """

        # expect_repl deals with odd case probably for code.py autorun
        self.sendrepl("\x04", expect_repl=expect_repl)

    def ctrlc(self, expect_repl=True):
        """ restart the python interpreter on target by sending CTRL+C """

        # expect_repl deals with odd case probably for code.py autorun
        self.sendrepl("\x03", expect_repl=expect_repl)

    def start_app_on_powerup(self, appname):
        """ provide a system startup file (eg. code.py etc.) for the
            component this testboard is concerned with.
            As a result of calling this method, the pyexpect
            session will most likely hang as the target system
            will start the app as soon as the code.py/main.py appears """

        if self.m_homedir:
            with tempfile.NamedTemporaryFile("w") as startupfile:
                startupfile.write("import os\n")
                startupfile.write(f"os.chdir(\"{self.m_homedir}\")\n")
                startupfile.write(f"import {appname}\n")
                startupfile.seek(0)
                tgtmain = os.path.join(self.m_mountpoint, self.m_auto_run_file)
                self.m_fileops.copyfile(startupfile.name, tgtmain)


    def close_expect_serial(self):
        """ kill serial repl expect session, close serial port """

        # kill expect, release the serial port
        del self.m_child
        self.close_serial()

    def minicomserial(self):
        """ interact with serial port using minicom """

        self.close_expect_serial()

        #
        # start minicom
        # TODO better transfer of control to minicom, minirc etc.
        #
        os.system("minicom ACM0")

    def readserial(self):
        """ very crude serial port monitor """

        self.close_expect_serial()

        self.open_serial()

        while True:
            out = ""
            while self.m_ser.inWaiting() > 0:
                try:
                    char = self.m_ser.read(1).decode()

                # maybe the snake causes this
                except UnicodeDecodeError:
                    pass

                out += char

            if out != '':
                print(out, end="")
#
# Circuit Python board
#
class TestBoardCP(TestBoard):
    """ A CircuitPython scout radio test board """

    def __init__(self, serialport):
        """ Create a CircuitPython scout radio test board """

        mountpoint = sysdetect.wait_get_cp_mountpoint()

        if not mountpoint:
            sys.exit("Error: Circuit python filesystem mount not found")

        autorunfile_name = "code.py"

        #
        # A bit rude, but we want access. This may help.
        #
        autorunfile = os.path.join(mountpoint, autorunfile_name)

        if os.path.exists(autorunfile):
            os.unlink(autorunfile)

        #
        # Set mountpoint and fileops object member variables in base class
        # by passing them to the base class constructor.
        #
        # pylint seems to prefer this.
        #
        super().__init__(serialport,
                         mountpoint,
                         fileops.FileOPsCP(),
                         autorunfile_name)


    def sendrepl(self, cmd, expect_repl=True):
        """ send a command to CircuitPython repl """

        return self.sendreplbase(cmd + "\r\n", expect_repl)

#
# Micro Python board
#
class TestBoardMP(TestBoard):
    """ A MicroPython scout radio test board """

    def exit_rshell(self):
        """ kill rshell session - must be there """
        #
        # get out of rshell:
        # back to linux/windows shell with control-D
        #
        self.m_rshell_child.sendline("\x04\r\n")

        #
        # done with the rshell expect session
        #
        del self.m_rshell_child


    def __init__(self, serialport):
        """ Create a MicroPython scout radio test board """

        #
        # work around odd initial condition with serial
        # BEWARE this costs about 0.5s but worth it for consistent behaviour
        #
        self.create_pexpect_rshell_child()
        self.exit_rshell()

        #
        # come up with a python expect session
        #
        self.m_expect_session_type = "python"

        #
        # Set serial port, mountpoint, fileops object member variables
        # in base class by passing them to the base class constructor.
        #
        # pylint seems to prefer this.
        #
        super().__init__(serialport,
                         "/pyboard",
                         fileops.FileOPsMP(self),
                         "main.py")


    def create_pexpect_rshell_child(self):
        """ create a pexpect child object for MicroPython """

        try:
            self.m_rshell_child = pexpect.spawn("rshell", timeout=1)

        except pexpect.exceptions.ExceptionPexpect as pexpect_excep:
            if "The command was not found or was not executable" in repr(pexpect_excep):
                sys.exit("Error: rshell: command not found. Please install rshell")
        #
        # At least we didn't exception on the spawn...continue
        #
        self.m_rshell_child.expect("> ")

        if "No MicroPython boards connected" in self.m_rshell_child.before.decode():
            sys.exit("Error: rshell: No MicroPython boards connected")


    def set_expect_session_type(self, sessiontype):
        """ switch between rshell and python repl in Micro Python env """

        # happy path
        if self.m_expect_session_type == sessiontype:
            return

        if sessiontype == "rshell":
            #
            # switching from python repl on serial port to rshell app
            #

            # kill the serial port session with the python interpreter
            del self.m_child
            self.close_serial()

            # create the rshell session
            self.create_pexpect_rshell_child()

            #
            # remember we are now in rshell
            #
            self.m_expect_session_type = "rshell"

        if sessiontype == "python":
            #
            # switching from rshell app to python repl on serial port
            #
            self.exit_rshell()

            #
            # Create expect session on serial port for python again.
            # TODO HACK Not sure why sending a CR here gets pexpect confused.
            # Could be to do with the way the initial python pexpect session
            # was closed.
            #
            self.create_pexpect_child(send_cr=False)

            #
            # remember we are now in python mode on serial port
            #
            self.m_expect_session_type = "python"

            #
            # reboot here as rshell has been using the board
            #
            self.reboot()


    def sendrshellcmd(self, cmd, timeout = 10):
        """ send a command to rshell """

        self.set_expect_session_type("rshell")

        if VERBOSE_SEND_RSHELL:
            print(f"rshell: sending {cmd}")

        self.m_rshell_child.sendline(cmd)

        # can take a while to copy files in rshell
        self.m_rshell_child.expect("> ", timeout)

        response = self.m_rshell_child.before.decode()

        if VERBOSE_SEND_RSHELL_RESPONSE:
            print(response)

        return response

    def sendrepl(self, cmd, expect_repl=True):
        """ send a command to MicroPython repl """

        self.set_expect_session_type("python")

        return self.sendreplbase(cmd + "\r\n", expect_repl)


    def reboot(self, expect_repl=True):
        """ restart the python interpreter on target by sending CTRL+D """

        # expect_repl deals with odd case probably for code.py autorun

        #
        # MicroPython CTRL+D doesn't need CR tacked on.
        #
        self.sendreplbase("\x04", expect_repl=expect_repl)


# capitals keeps pylint happy
G_BOARD = None

def getboard( serialport="/dev/ttyACM0" ):
    """ return a singleton test board, instantiating it if required """
    global G_BOARD

    if os.path.exists(serialport):
        if not G_BOARD:
            if sysdetect.circuitpython():
                #
                # Create a CircuitPython board
                #
                G_BOARD = TestBoardCP(serialport)
            else:
                #
                # Create a MicroPython board
                #
                G_BOARD = TestBoardMP(serialport)

    if not G_BOARD:
        sys.exit("Error: board not found")

    return G_BOARD


if __name__ == "__main__":
    myboard = getboard()

    if not myboard:
        print("No MicroPython/CircuitPython test boards found")
    else:
        myboard.initialise()
        myboard.identify()
        serialportname = myboard.serialportname()
        print(f"repl available on serial port {serialportname}")
