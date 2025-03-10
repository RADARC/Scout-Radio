import os
components = ['Display', 'GPS', 'images', 'lib', 'LSM303', 'Morse', 'Radio']

def installcomponent(component):
    installfile = "install.py"

    if os.path.exists(os.path.join(component, installfile)):
        print(f"installing {component}")
        os.system(f"cd {component}; python3 {installfile}")
        #os.chdir(os.path.dirname(installfile))
        #exec(open(os.path.basename(installfile)).read())

for component in components:
    installcomponent(component)
