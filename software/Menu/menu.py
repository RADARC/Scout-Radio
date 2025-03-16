import board
import busio
import displayio
from adafruit_st7789 import ST7789
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
#from adafruit_display_group import DisplayGroup
from adafruit_display_text import label
from digitalio import DigitalInOut, Direction, Pull
import terminalio
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


# Button setup
button_a = DigitalInOut(board.GP2)
button_b = DigitalInOut(board.GP3)
button_c = DigitalInOut(board.GP6)
button_a.direction = Direction.INPUT
button_a.pull = Pull.UP
button_b.direction = Direction.INPUT
button_b.pull = Pull.UP
button_c.direction = Direction.INPUT
button_c.pull = Pull.UP
# Menu items
menu_items = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
selected_index = 0

# Function to update display
def update_display():
    display_group = displayio.Group()
    for index, item in enumerate(menu_items):
        text_color = 0xFFFFFF if index == selected_index else 0xAAAAAA
        text_label = label.Label(terminalio.FONT, text=item, color=text_color, x=20, y=20 + index * 30)
        display_group.append(text_label)

# Initial display
update_display()

while True:
    if button_a.value:  # Up button
        selected_index = (selected_index - 1) % len(menu_items)
        update_display()
    elif button_b.value:  # Select button
        print(f"Selected: {menu_items[selected_index]}")
    elif button_c.value:  # Down button
        selected_index = (selected_index + 1) % len(menu_items)
        update_display()
