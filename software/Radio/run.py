"""
run up a radio - this file is derived from test.py. i.e. test.py without
the formal test aspect.
Runs on host, full fat python.
"""

import runlib
import install

if __name__=="__main__":
    runlib.runapp("radioapp",
                install.homedir(),
                install.files() + install.supportfiles())
