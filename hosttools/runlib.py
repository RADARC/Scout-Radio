""" run an application on target """
import sys
import os
import argparse
import testboard

SERIALPORT = "/dev/ttyACM0"

def install_help(app):
    """ --install help text """
    return f"install {app} target files then run {app} (by 'import {app}')"

def revsync_help(app):
    """ --revsync help text """
    return f"copy {app} target files to host - use with care"

def app_help(app):
    """ --app help text """
    return f"autorun {app} on boot - installs autogenerated code.py/main.py"

def minicom_help(app):
    """ --minicom help text """
    return f"""interact with {app} using minicom rather than plain serial
            port dump. Use --minicom='<minicom-options>' eg.
            --minicom='-C output' to capture output"""

def run_help(app):
    """ --run help text """
    return f"run the app specified (by 'import myspecifiedapp') rather than {app}"

def repl_help():
    """ --repl help text """
    return """get python repl in minicom, don't run any app,
              same as --norun --minicom apart from minicom options cannot be
              specified."""

def norun_help():
    """ --norun help text """
    return "don't run any app, scrape serial port (non-interactive)"

def noboot_help():
    """ --noboot help text """
    return "don't reboot the board during initialisation"

def force_help():
    """ --force help text """
    return """Forcibly remove main.py for Micro Python boards.
            code.py is always removed for Circuit Python boards."""

def runapp(appname_p, homedir, installfiles):
    """ run specified application """

    appname = os.path.splitext(appname_p)[0]

    #
    # arguments:
    # appname: "import appname" must work on target to run the app
    # homedir: eg. /Radio,  Top level directory. Specified in Radio/install.py on host.
    # installfiles: specified in Radio/install.py on host
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", help=install_help(appname), action="store_true")
    parser.add_argument("--revsync", help=revsync_help(appname), action="store_true")
    parser.add_argument("--app",     help=app_help(appname), action="store_true")
    parser.add_argument("--minicom",  help=minicom_help(appname), nargs='*')
    parser.add_argument("--run",  help=run_help(appname), type=str)
    parser.add_argument("--norun",  help=norun_help(), action="store_true")
    parser.add_argument("--repl",  help=repl_help(), action="store_true")
    parser.add_argument("--noboot",  help=noboot_help(), action="store_true")
    parser.add_argument("--force",  help=force_help(), action="store_true")

    args = parser.parse_args()

    force = False
    if args.force:
        force = True

    board = testboard.getboard(SERIALPORT, force)

    # must get one
    assert board

    # eg. /Radio on target, Scout-Radio/software/Radio on host
    board.sethomedir(homedir)

    #
    # give board object its info
    #
    if args.install or args.revsync:
        board.setfiles(installfiles)

    # pull files back from target?
    if args.revsync:
        board.revsync()
        sys.exit(0)

    #
    # bring up the board
    # copy files to target if any are specified in setfiles method
    #
    if args.noboot:
        reboot = False
    else:
        reboot = True

    board.initialise(do_reboot=reboot)

    if args.run:
        app_to_run = os.path.splitext(args.run)[0]
    else:
        app_to_run = appname

    if args.app:

        board.start_app_on_powerup(app_to_run)

        print(f"{app_to_run} set to run on boot")

        #
        # pyexpect will most likely time out here as the app will
        # now be running on target.
        #
        sys.exit(0)

    #
    # default case
    # start the app, we won't get a >>> back
    #
    if not args.repl and not args.norun:
        board.sendrepl(f"import {app_to_run}", expect_repl=False)

    # runs until user interrupt
    if isinstance(args.minicom, list):
        board.minicomserial(args.minicom)
    elif args.repl:
        #
        # a bit hacky - no minicom opts possible
        #
        board.minicomserial([])
    else:
        board.readserial()
