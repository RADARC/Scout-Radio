import board
import busio
import displayio
import adafruit_st7789
from adafruit_button import Button
from adafruit_display_group import DisplayGroup
from adafruit_display_text import label
import terminalio

# Display setup
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
display = adafruit_st7789.ST7789(spi, rotation=180, width=240, height=240, cs=board.CE0, dc=board.DC, rst=board.RST)

# Button setup
button_a = board.BUTTON_A
button_b = board.BUTTON_B
button_c = board.BUTTON_C

# Menu items
menu_items = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
selected_index = 0

# Function to update display
def update_display():
    display_group = DisplayGroup()
    for index, item in enumerate(menu_items):
        text_color = 0xFFFFFF if index == selected_index else 0xAAAAAA
        text_label = label.Label(terminalio.FONT, text=item, color=text_color, x=20, y=20 + index * 30)
        display_group.append(text_label)
    display.show(display_group)

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
