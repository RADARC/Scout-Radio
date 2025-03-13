""" installer for Morse component """

# Environment: host python3

import sys
import installer

def files():
    """ source files """
    return [
        "MorseFlash.py"
      ]

def homedir():
    """ source directory """
    return "Morse"

if __name__=="__main__":
    installer.installfiles(sys.argv, homedir(), files())
