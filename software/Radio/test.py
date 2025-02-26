"""
  A unit test framework for the scout radio project built on pyunit.
  https://docs.python.org/3/library/unittest.html
  It uses a 'testboard' object to communicate with scout radios ("targets")
  Runs on host, full fat python.
"""
import unittest
import time
import testboard

# hack - should be able to run unit tests in any order eventually
#unittest.TestLoader.sortTestMethodsUsing = None

TARGETFILES = ["../lib/radarcplatform.py", "harness.py", "../lib/si4735_CP.py"]

SERIALPORT = "/dev/ttyACM0"

def formatoutput(output):
    """ format output from target board """
    for line in output.decode().split("\r\n"):
        print(line)

# hack so setUp main contents only run once...lots of ways to do this
board = None

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
class Si4735test(unittest.TestCase):

    def setUp(self):
        """ copy test files to target; grab a radio in the repl for testing """

        global board

        if not board:
            board = testboard.getboard(SERIALPORT)

            # must get one
            assert board

            board.setfiles(TARGETFILES)

            board.initialise()

            #
            # grab a singleton si4735 device as our first job
            #
            board.sendrepl('import harness')
            text = board.sendrepl('radio = harness.getradio()')
            formatoutput(text)

    def test01(self):
        """ reset radio """
        text = board.sendrepl('radio.reset()')
        formatoutput(text)

    def test03(self):
        """ test report firmware """
        text = board.sendrepl("harness.reportfirmware(radio)")
        formatoutput(text)

    def test04(self):
        """ patchPowerUp """
        text = board.sendrepl("radio.patchPowerUp()")
        formatoutput(text)

    def test05(self):
        """ downloadPatch """
        text = board.sendrepl("radio.downloadPatch()")
        formatoutput(text)

    def test06(self):
        """ tune an FM station """
        #
        # FIXME: improve quality by switching to radio 4
        #
        text = board.sendrepl("harness.testfm(radio, 10440)")
        formatoutput(text)

    def test07(self):
        """ report RSSI """
        text = board.sendrepl('radio.getCurrentReceivedSignalQuality(0)["rssi"]')
        formatoutput(text)

    def test08(self):
        """ report RSSI and RDS """
        text = board.sendrepl('harness.sigrssi(radio)')
        formatoutput(text)

    def test09(self):
        """ set volume low-ish """
        text = board.sendrepl('radio.setVolume(32)')
        formatoutput(text)

    def test10(self):
        """ test ssb stuff """
        #
        # NOTE time.sleep's can be done either on host or target.
        # probably host makes more sense?
        #
        text = board.sendrepl('radio.reset()')
        formatoutput(text)

        text = board.sendrepl('radio.patchPowerUp()')
        formatoutput(text)

        text = board.sendrepl('radio.downloadPatch()')
        formatoutput(text)

        text = board.sendrepl('radio.setSSB(2)')
        formatoutput(text)

        text = board.sendrepl('radio.setFrequency(14000)')
        formatoutput(text)

        text = board.sendrepl('radio.setSSBConfig(1, 0, 0, 1, 0, 1)')
        formatoutput(text)

        time.sleep(2)
        text = board.sendrepl('radio.setSSBAudioBandwidth(2)')
        formatoutput(text)

        print("bandwidth 2")
        time.sleep(2)
        text = board.sendrepl('radio.setSSBAudioBandwidth(3)')
        formatoutput(text)

        print("bandwidth 3")
        time.sleep(2)

        text = board.sendrepl('radio.setSSBAudioBandwidth(4)')
        formatoutput(text)
        print("bandwidth 4")
        time.sleep(2)

        text = board.sendrepl('radio.setSSBAudioBandwidth(1)')
        formatoutput(text)
        print("bandwidth 1")
        time.sleep(2)

    #
    # back to FM to finish with
    #
    def test11(self):
        self.test01()
        self.test06()

    def test12(self):
        self.test09()

    def test13(self):
        # Test SSB Sideband switching
        text = board.sendrepl('radio.reset()')
        formatoutput(text)

        text = board.sendrepl('radio.patchPowerUp()')
        formatoutput(text)

        text = board.sendrepl('radio.downloadPatch()')
        formatoutput(text)

        # Set LSB
        text = board.sendrepl('radio.setSSB(1)')
        formatoutput(text)

        text = board.sendrepl('radio.setFrequency(14000)')
        formatoutput(text)

        time.sleep(10)

         # Set USB
        text = board.sendrepl('radio.setSSB(2)')
        formatoutput(text)

        text = board.sendrepl('radio.setFrequency(14000)')
        formatoutput(text)

        time.sleep(10)





if __name__=="__main__":
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
