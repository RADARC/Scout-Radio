""" installer for images component """

# Environment: host python3

import sys
import installib

def homedir():
    """ source directory """
    return "images"

def files():
    """ source files """
    return [
        "Newlogo.bmp", "RADARC_Logo.bmp", "Scout_Logo.bmp"
      ]

if __name__=="__main__":
    installib.installfiles(sys.argv, homedir(), files())
