""" helper for component install.py's """

import testboard

def installfiles(argv, homedir, files, expect_repl=True):
    """ install or revsync files/directories from homedir source (component) """

    board = testboard.getboard()

    assert board

    board.sethomedir(homedir)
    board.setfiles(files)

    #
    # consider introducing --app optionc on install.py's to indicate
    # the component should be installed as the system application
    # i.e. the "active" application
    #

    # we should really use argparse properly...
    if len(argv) > 1 and "--revsync" in argv[1:]:
        board.revsync()
    else:
        board.initialise(expect_repl)

        board.reboot(expect_repl)
