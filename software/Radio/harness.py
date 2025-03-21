"""
test harness/library of test functions for si4735.
Runs on CircuitPython or MicroPython
"""
#TODO Change to drive UI functions in the radio.scout module

import time
import si47xx
from radarcplatform import circuitpython, micropython

if circuitpython():
    import board
    from busio import I2C
    from digitalio import DigitalInOut, Direction
    import microcontroller
    #microcontroller.cpu.frequency = 250_000_000  # run at 250 MHz instead of 125 MHz
    #microcontroller.cpu.frequency = 200_000_000  # run at 200 MHz instead of 125 MHz
    #microcontroller.cpu.frequency = 150_000_000  # run at 150 MHz instead of 125 MHz
    microcontroller.cpu.frequency = 150_000_000  # run at 150 MHz instead of 125 MHz

elif micropython():
    from machine import Pin, I2C


G_SI4735 = None

# grab a singleton si4735
def getsi4735():
    """ return a singleton si47xx device """
    global G_SI4735

    if not G_SI4735:
        if circuitpython():
            reset_pin = DigitalInOut(board.GP17)
            reset_pin.direction = Direction.OUTPUT
            i2c = I2C(board.GP19, board.GP18, frequency=1000000)
            i2c_address = 0x63

            #
            # FIXME
            # If we don't do this, the torch flashes randomly
            # whilst programming the si47xx. Need to find out
            # why this is happening - it shouldn't.
            #
            torch = DigitalInOut(board.GP16)
            torch.direction = Direction.OUTPUT
            torch.value = False

        if micropython():
            reset_pin = Pin(15, Pin.OUT, Pin.PULL_UP)
            i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=1000000)
            i2c_address = 0x11

        G_SI4735 = si47xx.SI4735(i2c, i2c_address, reset_pin)

    return G_SI4735

def getradio():
    return radio.RADIO(getsi4735())

def testfm(si4735, freq):
#    si4735.reset()
    si4735.setFM()
    #si4735.getFirmware()

    si4735.setRDSConfig(1,3,3,3,3)
    si4735.setFrequency(freq)

def test(si4735, freq):
    testfm(si4735, freq)

def test2():
    si4735 = getsi4735()

    #freq = 9391
    si4735.reset()

    addr = si4735.get_device_i2c_address()

    assert addr

    print("Address is ",addr)
    si4735.patchPowerUp()
    si4735.download_compressed_patch()

    si4735.setSSB(2)
    si4735.setFrequency(14000)

    si4735.setSSBConfig(1, 0, 0, 1, 0, 1)

    time.sleep(2)
    si4735.setSSBBandwidth(2)
    print("bandwidth 2")
    time.sleep(2)
    si4735.setSSBBandwidth(3)
    print("bandwidth 3")
    time.sleep(2)
    si4735.setSSBBandwidth(4)
    print("bandwidth 4")
    time.sleep(2)
    si4735.setSSBBandwidth(1)
    print("bandwidth 1")
    time.sleep(2)

    si4735.setAM()
    si4735.setFrequency(198)
    time.sleep(2)

    si4735.setFM()
    fwrev = si4735.getFirmware()
    print(fwrev)

    si4735.setRDSConfig(1,3,3,3,3)
    si4735.setFrequency(10420)

def sigrssi(si4735):

    print(si4735.getCurrentReceivedSignalQuality(0)["rssi"])

    si4735.getRDSStatus(0,0,0)
    print(si4735.station_name)
    print(si4735.station_text)

def contrssi(si4735):
    while True:
        sigrssi(si4735)
        time.sleep(1)

def reportfirmware(si4735):
    fwrev = si4735.getFirmware()
    print(fwrev)

# si4735 = getsi4735()
# si4735.reset()
# fwrev = si4735.getFirmware()
# si4735.patchPowerUp()
# si4735.downloadPatch()
# freq=9700
# si4735.setRDSConfig(1,3,3,3,3)
# test(si4735, freq)
# contrssi(getsi4735())
