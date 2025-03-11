import testboard

def installfiles(homedir, files):
    board = testboard.getboard()

    # must get one
    assert board

    board.setfiles(homedir, files)

    board.initialise()

    # reboot
    board.reboot()
