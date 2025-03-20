"""
run up GPS
Runs on host, full fat python.
"""

import runlib
import install

if __name__=="__main__":
    runlib.runapp("gps_simpletest", install.homedir(), install.files())
