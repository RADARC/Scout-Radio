""" helper for component install.py's """

import os
import argparse
import testboard

def revsync_help(app):
    """ --revsync help text """
    return f"copy {app} target files to host - use with care"


def installfiles(homedir, files, expect_repl=True):
    """ install or revsync files/directories from homedir source (component) """

    appname = os.path.splitext(homedir)[0]

    # arguments:
    # homedir: eg. /Radio,  Top level directory. Specified in Radio/install.py on host.
    # files: specified in Radio/install.py on host
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("--revsync", help=revsync_help(appname), action="store_true")
    args = parser.parse_args()

    board = testboard.getboard()

    assert board

    board.sethomedir(homedir)
    board.setfiles(files)

    if args.revsync:
        board.revsync()
    else:
        board.initialise(expect_repl)

        board.reboot(expect_repl)
