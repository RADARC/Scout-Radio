# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Bitmap test
"""
import board
import busio
import terminalio
import displayio

# Starting in CircuitPython 9.x fourwire will be a seperate internal library
# rather than a component of the displayio library
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789

# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GP9
tft_dc = board.GP8
spi_mosi = board.GP11
spi_clk = board.GP10
spi = busio.SPI(spi_clk, spi_mosi)
backlight = board.GP13

display_bus = FourWire(spi, command=tft_dc, polarity = 1, phase = 1, reset=board.GP12)

display = ST7789(display_bus, width=240, height=240,rowstart=80, rotation=90, backlight_pin=backlight)


# Set the backlight
display.brightness = 0.8


# Make the display context
splash = displayio.Group()
display.root_group = splash

odb = displayio.OnDiskBitmap('/RADARC_Logo.bmp')
face = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)

#odb = displayio.OnDiskBitmap('/Scout_Logo.bmp')
#face = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
splash.y = 0
splash.append(face)

# Wait forever
while True:
    pass

