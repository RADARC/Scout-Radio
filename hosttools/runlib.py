""" run an application on target """
import sys
import testboard

# hack - should be able to run unit tests in any order eventually
#unittest.TestLoader.sortTestMethodsUsing = None

SERIALPORT = "/dev/ttyACM0"

def usage():
    """ help text - should use argparse """
    print("use --install to install target files")
    print("use --revsync to pull them back to host")
    print("use --app to create code.py/main.py to autorun this app on boot")
    sys.exit(2)

def runapp(appname, homedir, installfiles):
    """ run specified application """
    DO_INSTALL = False
    DO_REVSYNC = False
    DO_AUTORUN = False

    if len(sys.argv) > 1:
        if "--install" in sys.argv[1:]:
            DO_INSTALL = True
        if "--revsync" in sys.argv[1:]:
            DO_REVSYNC = True
        if "--app" in sys.argv[1:]:
            DO_AUTORUN = True
        if "--help" in sys.argv[1:]:
            usage()

    BOARD = testboard.getboard(SERIALPORT)

    # must get one
    assert BOARD

    # /Radio on target: see install.py
    BOARD.sethomedir(homedir)

    # optionally install files
    # could specify different file lists here from install.py
    # if wanted.
    if DO_INSTALL or DO_REVSYNC:
        BOARD.setfiles(installfiles)

    # pull files back from target?
    if DO_REVSYNC:
        BOARD.revsync()
        sys.exit(0)

    # does copy files to target if any are specified in setfiles method
    BOARD.initialise()

    # once we've done developing, start the app on power up
    # -- puts a code.py/main.py on target
    if DO_AUTORUN:

        BOARD.start_app_on_powerup(appname)

        print(f"{appname} set to run on boot")

        #
        # pyexpect will most likely time out here as the app will
        # now be running on target.
        #
        sys.exit(0)

    #
    # start the app, we won't get a >>> back
    #
    BOARD.sendrepl(f"import {appname}", expect_repl=False)

    # runs until user interrupt
    BOARD.readserial()
