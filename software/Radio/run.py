"""
run up a radio - this file is derived from test.py. Test.py without the formal
test aspect.
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

    # /Radio on target: see install.py
    BOARD.sethomedir(install.homedir())

    # optionally install files
    # could specify different file lists here from install.py
    # if wanted.
    if DO_INSTALL or DO_REVSYNC:
        BOARD.setfiles(install.files() + install.supportfiles())

    # pull files back from target?
    if DO_REVSYNC:
        BOARD.revsync()
        sys.exit(0)

    # does copy files to target
    BOARD.initialise()

    # once we've done developing, start the app on power up
    # -- puts a code.py/main.py on target
    #BOARD.start_app_on_powerup("radioapp")

    #
    # start the app, we won't get a >>> back
    #
    BOARD.sendrepl('import radioapp', expect_repl=False)

    # #
    # # grab an si4735 device
    # #
    # BOARD.sendrepl('import harness')
    # text = BOARD.sendrepl('radio = harness.getradio()')
    # formatoutput(text)

    # #
    # # do some stuff
    # #
    # text = BOARD.sendrepl('radio.reset()')
    # formatoutput(text)

    # text = BOARD.sendrepl('radio.patchPowerUp()')
    # formatoutput(text)

    # text = BOARD.sendrepl('radio.downloadPatch()')
    # formatoutput(text)

    # text = BOARD.sendrepl('radio.setSSB(2)')
    # formatoutput(text)

    # text = BOARD.sendrepl('radio.setFrequency(14000)')
    # formatoutput(text)
