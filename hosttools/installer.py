import testboard

def installfiles(homedir, files):
    board = testboard.getboard()

    # must get one
    assert board

    board.setfiles(homedir, files)

    board.initialise()

    # reboot
    board.sendrepl("\x04\r\n\r\n")
