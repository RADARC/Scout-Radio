""" helper for component install.py's """

import testboard

def installfiles(argv, homedir, files, expect_repl=True):
    """ install or revsync files/directories from homedir source (component) """

    board = testboard.getboard()

    assert board

    board.setfiles(homedir, files)

    # we should really use argparse properly...
    if len(argv) > 1 and argv[1] == "--revsync":
        board.revsync()
    else:
        board.initialise(expect_repl)

        board.reboot(expect_repl)
