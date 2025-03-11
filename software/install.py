import sys
import installer

def files():
    return []

def files_norepl():
    return [
        "code.py"
      ]

def homedir():
    return ""

if __name__=="__main__":
    installer.installfiles_norepl(sys.argv, homedir(), files_norepl())
