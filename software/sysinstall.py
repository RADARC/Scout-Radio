""" install complete scout radio system """
import sys
import os

sr_components = ['Display', 'GPS', 'images', 'lib', 'LSM303', 'Morse', 'Radio']

def installcomponent(component):
    """ install one component of the scout radio system """

    installfile = "install.py"

    if os.path.exists(os.path.join(component, installfile)):
        print(f"Installing {component}")
        if component:
            return_code = os.system(f"cd {component}; python3 {installfile}")
        else:
            return_code = os.system(f"python3 {installfile}")

        #
        # propagate failure up
        #
        if return_code != 0:
            sys.exit(f"Install failed on component {component}")

#
# install components
#
for sr_component in sr_components:
    installcomponent(sr_component)
