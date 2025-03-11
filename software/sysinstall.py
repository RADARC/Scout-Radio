""" install complete scout radio system """
import sys
import os

TOPLEVEL = False

sr_components = ['Display', 'GPS', 'images', 'lib', 'LSM303', 'Morse', 'Radio']

def installcomponent(component):
    """ install one component of the scout radio system """

    installfile = "install.py"

    if os.path.exists(os.path.join(component, installfile)):
        print(f"Installing {component}")
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
for sr_component in sr_components:
    installcomponent(sr_component)

#
# install top level if required
#
if TOPLEVEL:
    print("Installing top level")

    top_level_rc = os.system("python3 install.py")

    if top_level_rc != 0:
        sys.exit("Install failed on top level install.py")
