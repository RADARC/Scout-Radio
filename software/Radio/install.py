""" installer for Radio component """

# Environment: host python3

import sys
import os
import installib

SIBINPATCH="patchcomp.bin"

#
# if patchcomp.bin does not exist, create it by running csg2bin.py
#
def files():
    """ source files """
    return [
        "si47xx.py", "harness.py", SIBINPATCH, "radioapp.py","radio.py"
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
      ]

if __name__=="__main__":
    if not os.path.exists(SIBINPATCH):
        print(f"{SIBINPATCH} does not exist. Please generate by running csg2bin.py")
        sys.exit(1)

    installib.installfiles(homedir(), files() + supportfiles())
    #installib.installfiles(homedir(), files())
