""" install complete scout radio system """
import sys
import os

#
# All this file does is automate the running of install.py in
# each of the components below, first 'cd' ing to its directory.
#
sr_components = ['Display', 'GPS', 'images', 'lib', 'LSM303', 'Morse', 'Radio']

def installcomponent(component):
    """ install one component of the scout radio system """

    installfile = "install.py"

    if os.path.exists(os.path.join(component, installfile)):
        print(f"Installing {component}")
        return_code = os.system(f"cd {component}; python3 {installfile}")

        #
        # propagate failure up
        #
        if return_code != 0:
            sys.exit(f"Install failed on component {component}")
#
# usage - not worth using argparse
#
if sys.argv and len(sys.argv) > 1:
    if sys.argv[1] in ["--help", "-h", "-?"]:
        print(f"{sys.argv[0]}: Install scout radio python software", file=sys.stderr)
        STR_COMPONENTS = ", ".join(sr_components)
        print(f"{sys.argv[0]}: \
The following components will be installed: {STR_COMPONENTS}", file=sys.stderr)

        print(f"{sys.argv[0]}: \
All this file does is go round individual components and invoke their \
install.py files", file=sys.stderr)

        print(f"{sys.argv[0]}: usage: python {sys.argv[0]}", file=sys.stderr)
        # traditional
        sys.exit(2)

#
# install components
#
for sr_component in sr_components:
    installcomponent(sr_component)
