""" methods to try and detect target hardware type """

import subprocess
import serial
import pexpect
import pexpect.fdpexpect

def sysdetect_circuitpython_serial(serialport):
    """ Detect via USB serial port if a board is running circuit python """
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = serialport

    try:
        ser.open()

    except serial.SerialException as excep:
        print(f"{excep}")
        return False

    try:
        child = pexpect.fdpexpect.fdspawn(ser, timeout=0.5)
        child.sendline("import sys\r\n")
        child.expect(">>>")
        child.sendline("print(sys.implementation.name)\r\n")
        child.expect(">>>")

    except pexpect.exceptions.TIMEOUT:
        return False

    return "circuitpython" in child.before.decode()


def sysdetect_circuitpython_usb():
    """ Detect via lsusb command if a board is running circuit python """

    # lighter weight than sysdetect_circuitpython_serial
    proc = subprocess.run(["lsusb"], shell = True, check = True, stdout=subprocess.PIPE)

    #
    # may not be too robust
    #
    return "Adafruit" in proc.stdout.decode()

def circuitpython():
    """ returns True if running on circuit python """

    return sysdetect_circuitpython_usb()

def get_cp_mountpoint():
    """ find circuit python filesystem mount """
    #
    # work out where the circuit python filesystem is mounted
    #
    mountpoint = None
    with open('/proc/mounts', 'r', encoding="utf-8") as mounts:
        for line in mounts.readlines():
            candidate_mp = line.strip().split()[1]
            if "CIRCUITPY" in candidate_mp:
                mountpoint = candidate_mp
                break

    return mountpoint
