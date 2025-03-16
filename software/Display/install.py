""" installer for Display component """

# Environment: host python3

import sys
import installer

def files():
    """ source files """
    return [
        "Splash.py", "st7789bmp.py"
      ]

def homedir():
    """ source directory """
    return "Display"

if __name__=="__main__":
    installer.installfiles(sys.argv, homedir(), files())
