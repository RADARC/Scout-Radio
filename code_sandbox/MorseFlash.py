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
import pwmio
import busio
from adafruit_display_text.label import Label
from displayio import Group, release_displays
from terminalio import FONT
from fourwire import FourWire
from adafruit_st7789 import ST7789

import supervisor
switch6 = DigitalInOut(board.GP22)
switch6.direction = Direction.INPUT
switch6.pull = Pull.UP


torch = DigitalInOut(board.GP16)
torch.direction = Direction.OUTPUT

# Configuration:
# Message to display (capital letters and numbers only)
message = 'RADARC 2025'
dot_length = 0.15  # Duration of one Morse dot
dash_length = (dot_length * 3.0)  # Duration of one Morse dash
symbol_gap = dot_length  # Duration of gap between dot or dash
character_gap = (dot_length * 3.0)  # Duration of gap between characters


# Encoder button setup
switch_enc = DigitalInOut(board.GP9)
switch_enc.direction = Direction.INPUT
switch_enc.pull = Pull.UP

# Initialise the display
release_displays()

#tft_cs = board.GP9
tft_dc = board.GP8
spi_mosi = board.GP11
spi_clk = board.GP10


spi = busio.SPI(spi_clk, spi_mosi)


display_bus = FourWire(spi, command=tft_dc, polarity = 1, phase = 1, reset=board.GP12)

display = ST7789(display_bus, width=240, height=240,rowstart=80, rotation=90)



# Create a main_group to hold anything we want to show on the display.
main_group = Group()

# Create a Label to show the page heading. If you have a very small
# display you may need to change to scale=1.
page_output_label = Label(FONT, text="Morse Code", scale=2)

# Place the page label near the top left corner with anchored positioning
page_output_label.anchor_point = (0, 0)
page_output_label.anchored_position = (0, 0)

# Add the pagelabel to the main_group
main_group.append(page_output_label)

message_output_label = Label(FONT, text= message, scale=2)

# Place the message label near the top left corner with anchored positioning
message_output_label.anchor_point = (0, 0)
message_output_label.anchored_position = (0, 50)

# Add the message label to the main_group
main_group.append(message_output_label)
# Set the main_group as the root_group of the display
display.root_group = main_group


tone = pwmio.PWMOut(board.GP20, duty_cycle=0, frequency=440, variable_frequency=False)



morse = [
    ('A', '.-'),
    ('B', '-...'),
    ('C', '-.-.'),
    ('D', '-..'),
    ('E', '.'),
    ('F', '..-.'),
    ('G', '--.'),
    ('H', '....'),
    ('I', '..'),
    ('J', '.---'),
    ('K', '-.-'),
    ('L', '.-..'),
    ('M', '--'),
    ('N', '-.'),
    ('O', '---'),
    ('P', '.--.'),
    ('Q', '--.-'),
    ('R', '.-.'),
    ('S', '...'),
    ('T', '-'),
    ('U', '..-'),
    ('V', '...-'),
    ('W', '.--'),
    ('X', '-..-'),
    ('Y', '-.--'),
    ('Z', '--..'),
    ('0', '-----'),
    ('1', '.----'),
    ('2', '..---'),
    ('3', '...--'),
    ('4', '....-'),
    ('5', '.....'),
    ('6', '-....'),
    ('7', '--...'),
    ('8', '---..'),
    ('9', '----.'),
]


# Define a class that represents the morse flasher.


class MorseFlasher:
   

    def light(self, on=False):
        if on:
            torch.value = True
            tone.duty_cycle = 65535 // 2  # On 50%
            
        else:
            torch.value = False
            tone.duty_cycle = 0
            if switch6.value is False:
                supervisor.set_next_code_file('prog_mgr.py')
                supervisor.reload()  
           
        

    def showDot(self):
        self.light(True)
        time.sleep(dot_length)
        self.light(False)
        time.sleep(symbol_gap)

    def showDash(self):
        self.light(True)
        time.sleep(dash_length)
        self.light(False)
        time.sleep(symbol_gap)

    def encode(self, string):
        output = ""
        # iterate through string's characters
        for c in string:
            # find morse code for a character
            for x in morse:
                if x[0] == c:
                    # add code to output
                    output += x[1]
            # add a space in between characters
            output += " "
        # save complete morse code output to display
        self.display(output)

    def display(self, code=".-.-.- "):
        # iterate through morse code symbols
        for c in code:
            # show a dot
            if c == ".":
                self.showDot()
            # show a dash
            elif c == "-":
                self.showDash()
            # show a gap
            elif c == " ":
                time.sleep(character_gap)




# Create a morse flasher object.
flasher = MorseFlasher()

# Main loop will run forever
while True:
    flasher.encode(message)
    