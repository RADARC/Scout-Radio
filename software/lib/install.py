""" installer for lib component """

# Environment: host python3

import sys
import installib

def homedir():
    """ source directory """
    return "lib"

def files():
    """ source files/directories """
    return ["radarcplatform.py",
            "adafruit_st7789.mpy",
            "adafruit_gps.mpy",
            "adafruit_lsm303dlh_mag.mpy",
            "adafruit_display_text"]

if __name__=="__main__":
    installib.installfiles(sys.argv, homedir(), files())
