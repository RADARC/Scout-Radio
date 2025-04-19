"""
abstractions to assist with CircuitPython (CP) MicroPython (MP) differences
"""

import sys

def circuitpython():
    """ returns True if we are running on CircuitPython """

    return 'circuitpython' in sys.implementation.name

def micropython():
    """ returns True if we are running on MicroPython """

    return 'micropython' in sys.implementation.name

def setpin(pin, val):
    """ utility to set truth value for CP and MP pins """

    truevals = [True, 1]
    falsevals = [False, 0]

    assert val in truevals + falsevals

    if micropython():
        if val in truevals:
            pin.value(1)
        if val in falsevals:
            pin.value(0)

    if circuitpython():
        if val in truevals:
            pin.value = True
        if val in falsevals:
            pin.value = False

class RADARCi2cdev:
    """ wrapper for i2c device handling """

    def __init__(self, i2cdev, addr):
        """ i2cdev is either a busio.I2C (CP) or machine.I2C (MP) instance """
        self.m_i2cdev = i2cdev
        self.m_device_address = addr

    def lock(self):
        """ should not usually be used externally """
        if circuitpython():
            while not self.m_i2cdev.try_lock():
                pass

    def unlock(self):
        """ should not usually be used externally """
        if circuitpython():
            self.m_i2cdev.unlock()

    def writeto(self, val):
        """ write bytearray to i2c """
        self.lock()

        result = self.m_i2cdev.writeto(self.m_device_address, val)

        self.unlock()

        return result

    def readfrom(self, transfersize):
        """ read bytearray of specified size from i2c """
        if micropython():
            return self.m_i2cdev.readfrom(self.m_device_address, transfersize)

        if circuitpython():
            storage = bytearray(transfersize)
            self.lock()
            self.m_i2cdev.readfrom_into(self.m_device_address, storage)
            self.unlock()
            return storage

        #
        # should never get here
        #
        assert False

        return None
