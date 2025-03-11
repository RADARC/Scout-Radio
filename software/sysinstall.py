import sys
import os

toplevel = False

components = ['Display', 'GPS', 'images', 'lib', 'LSM303', 'Morse', 'Radio']

def installcomponent(component):
    installfile = "install.py"

    if os.path.exists(os.path.join(component, installfile)):
        print(f"installing {component}")
        if component:
            rc = os.system(f"cd {component}; python3 {installfile}")
        else:
            rc = os.system(f"python3 {installfile}")

        #
        # propagate failure up
        #
        if rc != 0:
            sys.exit(f"Install failed on component {component}")

#
# install components
#
for component in components:
    installcomponent(component)

#
# install top level
#
if toplevel:
    rc = os.system(f"python3 install.py")

    if rc != 0:
        sys.exit(f"Install failed on top level install.py")
