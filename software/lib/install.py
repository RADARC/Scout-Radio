import sys
import installer

def homedir():
    return "lib"

def files():
    return ["radarcplatform.py", "si4735_CP.py", "adafruit_st7789.mpy",
            "adafruit_display_text"]

if __name__=="__main__":
    installer.installfiles(sys.argv, homedir(), files())
