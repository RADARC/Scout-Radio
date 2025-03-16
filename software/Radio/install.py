""" installer for Radio component """

# Environment: host python3

import sys
import installer

def files():
    """ source files """
    return [
        "harness.py", "patch.csg", "radioapp.py"
      ]

def homedir():
    """ source directory """
    return "Radio"

#
# may already be there....handy if we are working on them
#
def supportfiles():
    """ source files from lib - handy for development """
    return [
      ("../lib/radarcplatform.py", "/lib/radarcplatform.py"),
      ("../lib/si4735_CP.py", "/lib/si4735_CP.py"),
      ]

if __name__=="__main__":
    installer.installfiles(sys.argv, homedir(), files() + supportfiles())
    #installer.installfiles(sys.argv, homedir(), files())

