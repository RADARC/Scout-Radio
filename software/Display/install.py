""" installer for Display component """

# Environment: host python3

import sys
import installib

def files():
    """ source files """
    return [
        "Splash.py", "st7789bmp.py", "st7789test.py", "st7789testbl.py"
      ]

def homedir():
    """ source directory """
    return "Display"

if __name__=="__main__":
    installib.installfiles(homedir(), files())
