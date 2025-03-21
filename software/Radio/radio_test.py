"""
 Test radio object
 run with
   time python radio_test.py [--install]
"""
import unittest
import sys
import testboard
import install

DO_INSTALL = False

class Si47xxtest_download(unittest.TestCase):
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
            self.m_board.sendrepl('radio = harness.getradio()')


    def test100(self):
        """ reset si4735 """
        text = self.m_board.sendrepl('radio.reset()')
        self.assertTrue(text == "Reset")



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
