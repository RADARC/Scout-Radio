""" installer for LSM303 component """

# Environment: host python3

import sys
import installer

def files():
    """ source files """
    return [
        "lsm303_accel_simpletest.py",
        "lsm303dlh_mag_simpletest.py",
        "lsm303dlh_mag_compass.py"
      ]

def homedir():
    """ source directory """
    return "LSM303"

if __name__=="__main__":
    installer.installfiles(sys.argv, homedir(), files())
