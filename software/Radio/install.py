""" installer for Radio component """

# Environment: host python3

import sys
import os
import installer

COMPRESSED_PATCH="patchcomp.bin"

#
# if patchcomp.bin does not exist, create it by running csg2bin.py
#
def files():
    """ source files """
    return [
        "harness.py", COMPRESSED_PATCH, "radioapp.py","radio_rx.py"
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
    if not os.path.exists(COMPRESSED_PATCH):
        print(f"{COMPRESSED_PATCH} does not exist. Please generate by running csg2bin.py")
        sys.exit(1)

    installer.installfiles(sys.argv, homedir(), files() + supportfiles())
    #installer.installfiles(sys.argv, homedir(), files())
