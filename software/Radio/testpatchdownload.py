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
        # split off embedded CR/LF
        actual_hex = text.split('{')[0][:-2]
        expected_hex = "0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x10"
        self.assertTrue(expected_hex == actual_hex.strip())

    def test04(self):
        """ patchPowerUp """
        BOARD.sendrepl("radio.patchPowerUp()")

    def test05(self):
        """ downloadPatch """
        #text = BOARD.sendrepl("radio.downloadPatch()")
        #self.assertTrue(text == "Download patch")
        text = BOARD.sendrepl("radio.download_compressed_patch()")
        self.assertTrue(text == "Download compressed patch")

    def test06(self):
        """ test report firmware """
        text = BOARD.sendrepl("harness.reportfirmware(radio)")
        expected = "0x80, 0x20, 0x31, 0x30, 0x9d, 0x29, 0x36, 0x30, 0x41\r\n{'partnumber': '0x20', 'patchid': '0x9d29', 'firmware': '1.0', 'component': '6.0', 'chiprevision': 'A'}\r\n{'partnumber': '0x20', 'patchid': '0x9d29', 'firmware': '1.0', 'component': '6.0', 'chiprevision': 'A'}"
        self.assertTrue(text == expected)


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
