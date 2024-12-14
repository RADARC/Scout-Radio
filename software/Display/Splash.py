# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Bitmap test
"""
import board
import busio
import digitalio
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

# if PWM not used mute audio
PWM = digitalio.DigitalInOut(board.GP15)
PWM.direction = digitalio.Direction.OUTPUT
PWM.value = False

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

#odb = displayio.OnDiskBitmap('/RADARC_Logo.bmp')
#face = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)

odb = displayio.OnDiskBitmap('/Scout_Logo.bmp')
face = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
splash.y = 0
splash.append(face)

#Scout Bitmap
text_group = displayio.Group(scale=3, x=20, y=180)
text = "Scout Radio"
text_area = label.Label(terminalio.FONT, text=text, color=0x400090)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

# white background
inner_bitmap = displayio.Bitmap(240, 100, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xffffff  # white
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=0, y=160)
splash.append(inner_sprite)

# Text Scout group
text_group = displayio.Group(scale=3, x=0, y=240)
text = "2nd Woodley"
text_area = label.Label(terminalio.FONT, text=text, color=0xffffff)
text_group.append(text_area)  # Subgroup for text scaling
text_group.y = 137
text_group.x = 20
splash.append(text_group)

# Text Scout radio
text_group = displayio.Group(scale=3, x=0, y=240)
text = "Scout Radio"
text_area = label.Label(terminalio.FONT, text=text, color=0x400090)
text_group.append(text_area)  # Subgroup for text scaling
text_group.y = 210
text_group.x = 20
splash.append(text_group)

# Text select
text_group = displayio.Group(scale=2, x=0, y=240)
text = "<- Press to begin"
text_area = label.Label(terminalio.FONT, text=text, color=0x400090)
text_group.append(text_area)  # Subgroup for text scaling
text_group.y = 180
text_group.x = 0
splash.append(text_group)

# Wait forever
while True:
    pass

