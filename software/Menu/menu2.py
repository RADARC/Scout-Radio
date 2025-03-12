import board
import gc
import displayio
from adafruit_st7789 import ST7789
import busio
import rotaryio
import terminalio
from adafruit_display_text import label
from displayio import FourWire
# Release any resources currently in use for the displays
displayio.release_displays()

# Display setup
tft_cs = board.GP9
tft_dc = board.GP8
spi_mosi = board.GP11
spi_clk = board.GP10
spi = busio.SPI(spi_clk, spi_mosi)
backlight = board.GP13

display_bus = FourWire(spi, command=tft_dc, polarity = 1, phase = 1, reset=board.GP12)

display = ST7789(display_bus, width=240, height=240,rowstart=80, rotation=90, backlight_pin=backlight)

# Rotary encoder setup
encoder = rotaryio.IncrementalEncoder(board.GP15, board.GP14)
last_position = encoder.position

# Menu items
menu_items = ["AM Radio", "FM Radio", "Morse Code", "Torch", "GPS", "Compass","About"]
selected_index = 0

# Create display context
group = displayio.Group()
display.root_group = group

# function to create display
def create_menu():   
    for i, item in enumerate(menu_items):
        text_color = 0xFFFFFF if i == selected_index else 0xAAAAAA
 
        text_area = label.Label(terminalio.FONT, scale = 3, text=item, color=text_color, x=20, y=30 + i * 30)
        
        group.append(text_area)
       
# Function to update the display
def update_menu():
    
    
    for i, item in enumerate(menu_items):
        text_area = group.pop(i) 
        text_area.colour = 0xFFFFFF if i == selected_index else 0xAAAAAA
        
        
        
        
create_menu()

while True:
    current_position = encoder.position
    if current_position != last_position:
        selected_index = (selected_index + (current_position - last_position)) % len(menu_items)
        last_position = current_position
        update_menu()
        gc.collect()
        start_mem = gc.mem_free()
        print( "Available memory: {} bytes".format(start_mem) ) 