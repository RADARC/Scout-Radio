"""
run up morse
"""

import sys
import testboard
from testboard import formatoutput
import install

# hack - should be able to run unit tests in any order eventually
#unittest.TestLoader.sortTestMethodsUsing = None

SERIALPORT = "/dev/ttyACM0"

def usage():
    """ help text - should use argparse """
    print("use --install to install target files")
    print("use --revsync to pull them back to host")
    sys.exit(2)

if __name__=="__main__":

    DO_INSTALL = False
    DO_REVSYNC = False

    if len(sys.argv) > 1:
        if "--install" in sys.argv[1:]:
            DO_INSTALL = True
        if "--revsync" in sys.argv[1:]:
            DO_REVSYNC = True
        if "--help" in sys.argv[1:]:
            usage()

    BOARD = testboard.getboard(SERIALPORT)

    # must get one
    assert BOARD

    # /Radio on target: see install.py
    BOARD.sethomedir(install.homedir())

    # optionally install files
    # could specify different file lists here from install.py
    # if wanted.
    if DO_INSTALL or DO_REVSYNC:
        BOARD.setfiles(install.files())

    # pull files back from target?
    if DO_REVSYNC:
        BOARD.revsync()
        sys.exit(0)

    # does copy files to target if any are specified in setfiles method
    BOARD.initialise()

    # once we've done developing, start the app on power up
    # -- puts a code.py/main.py on target
    #BOARD.start_app_on_powerup("MorseFlash")

    #
    # start the app, we won't get a >>> back
    #
    BOARD.sendrepl('import MorseFlash', expect_repl=False)
