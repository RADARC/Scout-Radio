"""
test harness/library of test functions for si4735.
Runs on CircuitPython or MicroPython
"""
#TODO Change to drive UI functions in the radio.scout module

import time
import si4735_CP as si4735
from radarcplatform import circuitpython, micropython

if circuitpython():
    import board
    from busio import I2C
    from digitalio import DigitalInOut, Direction
elif micropython():
    from machine import Pin, I2C

G_RADIO = None

# grab a singleton radio
def getradio():
    """ return a singleton si4735 device """
    global G_RADIO

    if not G_RADIO:
        if circuitpython():
            reset_pin = DigitalInOut(board.GP17)
            reset_pin.direction = Direction.OUTPUT
            i2c = I2C(board.GP19, board.GP18, frequency=400000)
            i2c_address = 0x63

            #
            # FIXME
            # If we don't do this, the torch flashes randomly
            # whilst programming the si4735. Need to find out
            # why this is happening - it shouldn't.
            #
            torch = DigitalInOut(board.GP16)
            torch.direction = Direction.OUTPUT
            torch.value = False

        if micropython():
            reset_pin = Pin(15, Pin.OUT, Pin.PULL_UP)
            i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
            i2c_address = 0x11

        G_RADIO = si4735.SI4735(i2c, i2c_address, reset_pin)

    return G_RADIO

def testfm(radio, freq):
#    radio.reset()
    radio.setFM()
    #radio.getFirmware()

    radio.setRDSConfig(1,3,3,3,3)
    radio.setFrequency(freq)

def test(radio, freq):
    testfm(radio, freq)

def test2():
    radio = getradio()

    #freq = 9391
    radio.reset()

    addr = radio.get_device_i2c_address()

    assert addr

    print("Address is ",addr)
    radio.patchPowerUp()
    radio.download_compressed_patch()

    radio.setSSB(2)
    radio.setFrequency(14000)

    radio.setSSBConfig(1, 0, 0, 1, 0, 1)

    time.sleep(2)
    radio.setSSBAudioBandwidth(2)
    print("bandwidth 2")
    time.sleep(2)
    radio.setSSBAudioBandwidth(3)
    print("bandwidth 3")
    time.sleep(2)
    radio.setSSBAudioBandwidth(4)
    print("bandwidth 4")
    time.sleep(2)
    radio.setSSBAudioBandwidth(1)
    print("bandwidth 1")
    time.sleep(2)

    radio.setAM()
    radio.setFrequency(198)
    time.sleep(2)

    radio.setFM()
    fwrev = radio.getFirmware()
    print(fwrev)

    radio.setRDSConfig(1,3,3,3,3)
    radio.setFrequency(10420)

def sigrssi(radio):

    print(radio.getCurrentReceivedSignalQuality(0)["rssi"])

    radio.getRDSStatus(0,0,0)
    print(radio.station_name)
    print(radio.station_text)

def contrssi(radio):
    while True:
        sigrssi(radio)
        time.sleep(1)

def reportfirmware(radio):
    fwrev = radio.getFirmware()
    print(fwrev)

# radio = getradio()
# radio.reset()
# fwrev = radio.getFirmware()
# radio.patchPowerUp()
# radio.downloadPatch()
# freq=9700
# radio.setRDSConfig(1,3,3,3,3)
# test(radio, freq)
# contrssi(getradio())
