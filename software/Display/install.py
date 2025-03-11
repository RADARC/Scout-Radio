import sys
import installer

def files():
    return [
        "Splash.py", "st7789bmp.py"
      ]

def homedir():
    return "Display"

if __name__=="__main__":
    installer.installfiles(sys.argv, homedir(), files())
