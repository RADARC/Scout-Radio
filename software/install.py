""" top level installer """

# Environment: host python3

import sys
import installer

def files_norepl():
    """ autorun thing at some point, maybe. Nothing right now. """
    return [
      ]

def homedir():
    """ source directory: we are at the top level so empty string """
    return ""

if __name__=="__main__":
    installer.installfiles(sys.argv, homedir(), files_norepl(), expect_repl=False)
