"""
run up a radio - this file is derived from test.py. i.e. test.py without
the formal test aspect.
Runs on host, full fat python.
"""

import sys
import os
import runlib
import install
from install import SIBINPATCH

if __name__=="__main__":
    if not os.path.exists(SIBINPATCH):
        print(f"{SIBINPATCH} does not exist. Please generate by running csg2bin.py")
        sys.exit(1)

    runlib.runapp("radioapp",
                install.homedir(),
                install.files() + install.supportfiles())
