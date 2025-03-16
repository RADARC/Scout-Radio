"""
run a test file - this file is derived from test.py
"""

import sys
import testboard
from testboard import formatoutput
import install

# hack - should be able to run unit tests in any order eventually
#unittest.TestLoader.sortTestMethodsUsing = None

SERIALPORT = "/dev/ttyACM0"

if __name__=="__main__":

    DO_INSTALL = False
    DO_REVSYNC = False

    if len(sys.argv) > 1:
        if "--install" in sys.argv[1:]:
            DO_INSTALL = True
        if "--revsync" in sys.argv[1:]:
            DO_REVSYNC = True

    BOARD = testboard.getboard(SERIALPORT)

    # must get one
    assert BOARD

    BOARD.sethomedir(install.homedir())

    # optionally install files
    if DO_INSTALL or DO_REVSYNC:
        BOARD.setfiles(install.files() + install.supportfiles())

    # pull files back?
    if DO_REVSYNC:
        BOARD.revsync()
        sys.exit(0)

    # does copy files to target
    BOARD.initialise()

    #
    # grab a singleton si4735 device as our first job
    #
    BOARD.sendrepl('import harness')
    text = BOARD.sendrepl('radio = harness.getradio()')
    formatoutput(text)

    text = BOARD.sendrepl('radio.reset()')
    formatoutput(text)

    text = BOARD.sendrepl('radio.patchPowerUp()')
    formatoutput(text)

    text = BOARD.sendrepl('radio.downloadPatch()')
    formatoutput(text)

    text = BOARD.sendrepl('radio.setSSB(2)')
    formatoutput(text)

    text = BOARD.sendrepl('radio.setFrequency(14000)')
    formatoutput(text)
