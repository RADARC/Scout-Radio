# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials UART Serial example"""
import board
import busio
import digitalio


uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

while True:
    data = uart.read(32)  # read up to 32 bytes
    # print(data)  # this is a bytearray type

    if data is not None:
       

        # convert bytearray to string
        data_string = ''.join([chr(b) for b in data])
        print(data_string, end="")

       
