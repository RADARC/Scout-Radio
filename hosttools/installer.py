import testboard

def installfiles(homedir, files):
    board = testboard.getboard()

    assert board

    board.setfiles(homedir, files)

    board.initialise()

    board.reboot()

def installfiles_norepl(homedir, files):
    board = testboard.getboard()

    assert board

    board.setfiles(homedir, files)

    board.initialise(expect_repl=False)

    board.reboot(expect_repl=False)
