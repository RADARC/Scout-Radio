# SPDX-FileCopyrightText: 2017 Collin Cunningham for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Circuit Playground Express CircuitPython Morse Code Flasher
# This is meant to work with the Circuit Playground Express board:
#   https://www.adafruit.com/product/3333
# Needs the NeoPixel module installed:
#   https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
# Author: Collin Cunningham
# License: MIT License (https://opensource.org/licenses/MIT)

import time
from digitalio import DigitalInOut, Direction, Pull
import board
import supervisor

torch = DigitalInOut(board.GP16)
torch.direction = Direction.OUTPUT
torch.value = True

# Encoder button setup
switch_enc = DigitalInOut(board.GP9)
switch_enc.direction = Direction.INPUT
switch_enc.pull = Pull.UP

time.sleep(1)
while True:
    if switch_enc.value is False:
        torch.value = False
        supervisor.set_next_code_file('prog_mgr.py')
        supervisor.reload()    
