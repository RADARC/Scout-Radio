import testboard

def installfiles(argv, homedir, files):
    board = testboard.getboard()

    assert board

    board.setfiles(homedir, files)

    if len(argv) > 1 and argv[1] == "--revsync":
        board.revsync()
    else:
        board.initialise()

        board.reboot()


def installfiles_norepl(argv, homedir, files):
    board = testboard.getboard()

    assert board

    board.setfiles(homedir, files)

    if len(argv) > 1 and argv[1] == "--revsync":
        board.revsync()
    else:
        board.initialise(expect_repl=False)

        board.reboot(expect_repl=False)


