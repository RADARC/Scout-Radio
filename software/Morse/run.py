"""
run up MorseFlash
Runs on host, full fat python.
"""

import runlib
import install

if __name__=="__main__":
    runlib.runapp("MorseFlash", install.homedir(), install.files())
