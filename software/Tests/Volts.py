
import time
import analogio
from board import *

pin_bat = analogio.AnalogIn(A2)
pin_Vcc = analogio.AnalogIn(A3)
while(True):
    print("Battery Volts = ",pin_bat.value * 6.6 /65535)
    print("Processor Volt = ",pin_Vcc.value * 6.6 /65535)
    time.sleep(1)