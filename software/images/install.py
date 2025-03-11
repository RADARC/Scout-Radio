""" installer for images component """
import sys
import installer

def homedir():
    """ source directory """
    return "images"

def files():
    """ source files """
    return [
        "Newlogo.bmp", "RADARC_Logo.bmp", "Scout_Logo.bmp"
      ]

if __name__=="__main__":
    installer.installfiles(sys.argv, homedir(), files())
