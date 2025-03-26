""" installer for GPS component """

# Environment: host python3

import sys
import installib

def files():
    """ source files """
    return [
        "gps_displayio_simpletest.py",
        "gps_simpletest.py",
        # Can't have file named serial.py on host as this conflicts
        # with host python implementation.
        ("gps-serial.py", "serial.py"),
        "gps_satellitefix.py"
      ]

def homedir():
    """ source directory """
    return "GPS"

if __name__=="__main__":
    installib.installfiles(homedir(), files())
