""" installer for Morse component """

# Environment: host python3

import sys
import installib

def files():
    """ source files """
    return [
        "MorseFlash.py"
      ]

def homedir():
    """ source directory """
    return "Morse"

if __name__=="__main__":
    installib.installfiles(homedir(), files())
