"""
run up LSM303
Runs on host, full fat python.
"""

import runlib
import install

if __name__=="__main__":
    runlib.runapp("lsm303dlh_mag_simpletest", install.homedir(), install.files())
