# SPDX-FileCopyrightText: 2024
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_display_text.label import Label
from displayio import Group, release_displays
from terminalio import FONT
from fourwire import FourWire
from adafruit_st7789 import ST7789
import busio
import adafruit_gps
import supervisor
from digitalio import DigitalInOut, Direction, Pull


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



uart = busio.UART(board.GP0, board.GP1, baudrate=9600, timeout=10)
#i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART
#gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Set update rate to once a second 1hz (what you typically want)
gps.send_command(b"PMTK220,1000")




# Create a main_group to hold anything we want to show on the display.
main_group = Group()

# Create a Label to show the readings. If you have a very small
# display you may need to change to scale=1.
display_output_label = Label(FONT, text="", scale=2)

# Place the label near the top left corner with anchored positioning
display_output_label.anchor_point = (0, 0)
display_output_label.anchored_position = (4, 4)

# Add the label to the main_group
main_group.append(display_output_label)

# Set the main_group as the root_group of the display
display.root_group = main_group


last_print = time.monotonic()

# Begin main loop
while True:
    gps.update()
    if switch_enc.value is False:       
        supervisor.set_next_code_file('prog_mgr.py')
        supervisor.reload()
        
    current = time.monotonic()
    # Update display data every second
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            display_output_label.text = "Waiting for fix..."
            continue
        # We have a fix! (gps.has_fix is true)
        t = gps.timestamp_utc

        # Update the label.text property to change the text on the display
        display_output_label.text = f"Timestamp (UTC): \
            \n{t.tm_mday}/{t.tm_mon}/{t.tm_year} {t.tm_hour}:{t.tm_min:02}:{t.tm_sec:02}\
            \nLat: {gps.latitude:.6f}\
            \nLong: {gps.longitude:.6f}"
