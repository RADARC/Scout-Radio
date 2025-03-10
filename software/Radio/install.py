import installer

def files():
    return [
        "harness.py", "patch.csg", ("radio.scout.py", "radio.scout.py")
      ]

def homedir():
    return "Radio"

def supportfiles():
    return [
      ("../lib/radarcplatform.py", "/lib/radarcplatform.py"),
      ("../lib/si4735_CP.py", "/lib/si4735_CP.py"),
      ]

if __name__=="__main__":
    installer.installfiles(homedir(), files() + supportfiles())
    #installer.installfiles(homedir(), files())

