""" installer for Radio component """

# Environment: host python3

import sys
import os
import installib

PATCHCREATOR="csg2bin.py"
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
    thisdir = os.path.abspath(os.path.dirname(sys.argv[0]))

    # try creating patch if not found
    if not os.path.exists(os.path.join(thisdir, SIBINPATCH)):
        os.system(os.path.join(thisdir, "csg2bin.py"))

    # patch should have been created
    if not os.path.exists(os.path.join(thisdir, SIBINPATCH)):
        print(f"{SIBINPATCH} does not exist. Please generate by running csg2bin.py")
        sys.exit(1)

    installib.installfiles(homedir(), files() + supportfiles())

