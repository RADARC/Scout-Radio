"""
  A unit test framework for the scout radio project built on pyunit.
  https://docs.python.org/3/library/unittest.html
  It uses a 'testboard' object to communicate with scout radios ("targets")
  Runs on host, full fat python.
"""
import unittest
import time
import sys
import testboard
from testboard import formatoutput
import install

# hack - should be able to run unit tests in any order eventually
#unittest.TestLoader.sortTestMethodsUsing = None

DO_INSTALL = False

#
# TODO none of the tests are using pyunit methods
# * self.assertEqual
# * self.assertFalse
# * self.assertTrue
# etc...
#
# We are just running a bunch of stuff and failing if we get
# a traceback from the target device.
#
# https://docs.python.org/3/library/unittest.html
#
class Si47xxtest(unittest.TestCase):
    """ Si47xxtest object """

    def setUp(self):
        """ copy test files to target; grab a si4735 in the repl for testing """

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
            # grab a singleton si47xx device as our first job
            #
            self.m_board.sendrepl('import harness')
            self.m_board.sendrepl('si4735 = harness.getsi4735()')


    def test01(self):
        """ reset si4735 """
        text = self.m_board.sendrepl('si4735.reset()')
        self.assertTrue(text == "Reset")

    def test03(self):
        """ test report firmware """
        text = self.m_board.sendrepl("harness.reportfirmware(si4735)")
        formatoutput(text)
        actual_hex = text.split('{', maxsplit=1)[0][:-2]
        expected_hex = "0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x10"
        self.assertTrue(expected_hex == actual_hex)

    def test04(self):
        """ patchPowerUp """
        text = self.m_board.sendrepl("si4735.patchPowerUp()")
        formatoutput(text)

    def test05(self):
        """ downloadPatch """
        text = self.m_board.sendrepl("si4735.download_compressed_patch()")
        self.assertTrue(text == "Download compressed patch")

    def test06(self):
        """ test report firmware """
        text = self.m_board.sendrepl("harness.reportfirmware(si4735)")
        expected = "0x80, 0x20, 0x31, 0x30, 0x9d, 0x29, 0x36, 0x30, 0x41\r\n{'partnumber': '0x20', 'patchid': '0x9d29', 'firmware': '1.0', 'component': '6.0', 'chiprevision': 'A'}\r\n{'partnumber': '0x20', 'patchid': '0x9d29', 'firmware': '1.0', 'component': '6.0', 'chiprevision': 'A'}"
        self.assertTrue(text == expected)


    def test07(self):
        """ tune an FM station """
        #
        # FIXME: improve quality by switching to radio 4
        #
        text = self.m_board.sendrepl("harness.testfm(si4735, 10440)")
        formatoutput(text)

    def test08(self):
        """ report RSSI """
        text = self.m_board.sendrepl('si4735.getCurrentReceivedSignalQuality(0)["rssi"]')
        formatoutput(text)

    def test09(self):
        """ report RSSI and RDS """
        text = self.m_board.sendrepl('harness.sigrssi(si4735)')
        formatoutput(text)

    def test10(self):
        """ set volume low-ish """
        text = self.m_board.sendrepl('si4735.setVolume(32)')
        formatoutput(text)

    def test11(self):
        """ test ssb stuff """
        #
        # NOTE time.sleep's can be done either on host or target.
        # probably host makes more sense?
        #
        text = self.m_board.sendrepl('si4735.reset()')
        formatoutput(text)

        text = self.m_board.sendrepl('si4735.patchPowerUp()')
        formatoutput(text)

        text = self.m_board.sendrepl('si4735.download_compressed_patch()')
        formatoutput(text)

        text = self.m_board.sendrepl('si4735.setSSB(2)')
        formatoutput(text)

        text = self.m_board.sendrepl('si4735.setFrequency(14000)')
        formatoutput(text)

        text = self.m_board.sendrepl('si4735.setSSBConfig(1, 0, 0, 1, 0, 1)')
        formatoutput(text)

        time.sleep(2)
        text = self.m_board.sendrepl('si4735.setSSBBandwidth(2)')
        formatoutput(text)

        print("bandwidth 2")
        time.sleep(2)
        text = self.m_board.sendrepl('si4735.setSSBBandwidth(3)')
        formatoutput(text)

        print("bandwidth 3")
        time.sleep(2)

        text = self.m_board.sendrepl('si4735.setSSBBandwidth(4)')
        formatoutput(text)
        print("bandwidth 4")
        time.sleep(2)

        text = self.m_board.sendrepl('si4735.setSSBBandwidth(1)')
        formatoutput(text)
        print("bandwidth 1")
        time.sleep(2)

    #
    # back to FM to finish with
    #
    def test12(self):
        self.test01()
        self.test03()

    def test13(self):
        self.test09()

    def test14(self):
        # Test SSB Sideband switching
        text = self.m_board.sendrepl('si4735.reset()')
        formatoutput(text)

        text = self.m_board.sendrepl('si4735.patchPowerUp()')
        formatoutput(text)

        text = self.m_board.sendrepl('si4735.download_compressed_patch()')
        formatoutput(text)

        # Set LSB
        text = self.m_board.sendrepl('si4735.setSSB(1)')
        formatoutput(text)

        text = self.m_board.sendrepl('si4735.setFrequency(14000)')
        formatoutput(text)

         # Set USB
        text = self.m_board.sendrepl('si4735.setSSB(2)')
        formatoutput(text)

        text = self.m_board.sendrepl('si4735.setFrequency(14000)')
        formatoutput(text)



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
