"""
 Investigate tardy i2c patch loading
 run with
   time python si47xx_testpatchdownload.py [--install]
"""

import sys
from datetime import datetime
import unittest
import testboard
import install

DO_INSTALL = False

class Si47xxtestdownload(unittest.TestCase):
    """ Si47xxtest_download object """

    def setUp(self):
        """ copy test files to target; grab a radio in the repl for testing """

        self.m_board = testboard.getboard()

        # must get one
        assert self.m_board

        if not self.m_board.initialised():
            self.m_board.sethomedir(install.homedir())

            # optionally install files
            if DO_INSTALL:
                self.m_board.setfiles(install.files() + install.supportfiles())

            self.m_board.initialise()

            #
            # grab a si47xx device as our first job
            #
            self.m_board.sendrepl('import harness')
            self.m_board.sendrepl('si4735 = harness.getsi4735()')


    def test100(self):
        """ reset si4735 """
        text = self.m_board.sendrepl('si4735.reset()')
        self.assertTrue(text == "Reset")

    def test110(self):
        """ test report firmware """
        text = self.m_board.sendrepl("harness.reportfirmware(si4735)")
        # split off embedded CR/LF
        actual_hex = text.split('{', maxsplit=1)[0][:-2]
        expected_hex = "0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x10"
        self.assertTrue(expected_hex == actual_hex)

    def test120(self):
        """ patchPowerUp """
        self.m_board.sendrepl("si4735.patchPowerUp()")

    def test130(self):
        """ downloadPatch """

        start_time = datetime.timestamp(datetime.now())
        text = self.m_board.sendrepl("si4735.download_compressed_patch()")
        end_time = datetime.timestamp(datetime.now())
        elapsed = end_time - start_time
        print(f"Download took {elapsed:.4f} seconds")

        #
        # expect to complete in less than 1.5 seconds
        #
        self.assertTrue(elapsed < 1.5)
        self.assertTrue(text == "Download compressed patch")

    def test140(self):
        """ test report firmware """
        text = self.m_board.sendrepl("harness.reportfirmware(si4735)")
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
# python -m unittest test.Si47xxtest
# or
# python -m unittest test.Si47xxtest.test6
#
# for example
# or just plain old python test.py which is the __main__ case above
#
