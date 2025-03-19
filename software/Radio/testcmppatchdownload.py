"""
 Investigate tardy i2c patch loading
 run with 
   time python testpatchdownload.py [--install]
"""
import unittest
import time
import sys
import testboard
from testboard import formatoutput
import install

# hack - should be able to run unit tests in any order eventually
#unittest.TestLoader.sortTestMethodsUsing = None

SERIALPORT = "/dev/ttyACM0"

# singleton board
BOARD = None

DO_INSTALL = False

class Si4735test(unittest.TestCase):
    """ Si4735test object """

    def setUp(self):
        """ copy test files to target; grab a radio in the repl for testing """

        global BOARD

        if not BOARD:
            BOARD = testboard.getboard(SERIALPORT)

            # must get one
            assert BOARD

            BOARD.sethomedir(install.homedir())

            # optionally install files
            if DO_INSTALL:
                BOARD.setfiles(install.files() + install.supportfiles())

            BOARD.initialise()

            #
            # grab a singleton si4735 device as our first job
            #
            BOARD.sendrepl('import harness')
            text = BOARD.sendrepl('radio = harness.getradio()')
            formatoutput(text)

    def test01(self):
        """ reset radio """
        text = BOARD.sendrepl('radio.reset()')
        self.assertTrue(text == "Reset")

    def test03(self):
        """ test report firmware """
        text = BOARD.sendrepl("harness.reportfirmware(radio)")
        formatoutput(text)

    def test04(self):
        """ patchPowerUp """
        text = BOARD.sendrepl("radio.patchPowerUp()")
        formatoutput(text)

    def test05(self):
        """ downloadPatch """
        text = BOARD.sendrepl("radio.download_compressed_patch()")
        #self.assertTrue(text == "Download compressed patch")
        formatoutput(text)

    # disable this test for now as it hangs with compressed firmware
    # def test06(self):
    #     """ test report firmware """
    #     text = BOARD.sendrepl("harness.reportfirmware(radio)")
    #     formatoutput(text)


if __name__=="__main__":

    if len(sys.argv) > 1:
        if "--install" in sys.argv[1:]:
            DO_INSTALL = True
            sys.argv.remove("--install")

    unittest.main(failfast=True)

#
# need to install 'rshell' command line utility for micropython
#
# can invoke using
# python -m unittest test.Si4735test
# or
# python -m unittest test.Si4735test.test6
#
# for example
# or just plain old python test.py which is the __main__ case above
#
