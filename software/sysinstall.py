import sys
import os
components = ['Display', 'GPS', 'images', 'lib', 'LSM303', 'Morse', 'Radio']

def installcomponent(component):
    installfile = "install.py"

    if os.path.exists(os.path.join(component, installfile)):
        print(f"installing {component}")
        rc = os.system(f"cd {component}; python3 {installfile}")

        #
        # propagate failure up
        #
        if rc != 0:
            sys.exit(f"Install failed on component {component}")

for component in components:
    installcomponent(component)
