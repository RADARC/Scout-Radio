""" top level installer """
import sys
import installer

def files_norepl():
    """ just one file at top level: autorun thing """
    return [
        "code.py"
      ]

def homedir():
    """ we are at the top level so empty string """
    return ""

if __name__=="__main__":
    installer.installfiles(sys.argv, homedir(), files_norepl(), expect_repl=False)
