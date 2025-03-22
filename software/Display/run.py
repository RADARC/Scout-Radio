"""
run up Display
Runs on host, full fat python.
"""

import runlib
import install

if __name__=="__main__":
    runlib.runapp("Splash", install.homedir(), install.files())
