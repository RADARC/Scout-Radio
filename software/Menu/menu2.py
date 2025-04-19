import board
import time
import gc
import displayio
from digitalio import DigitalInOut, Direction, Pull
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

# Encoder button setup
switch_enc = DigitalInOut(board.GP9)
switch_enc.direction = Direction.INPUT
switch_enc.pull = Pull.UP

# Menu items
menu_items = ["AM Radio", "FM Radio", "Morse Code", "Torch", "GPS", "Compass","About"]
selected_index = 0



# function to create display
def display_splash():
    
    splash = displayio.Group()
    display.root_group = splash
    
    # RADARC Bitmap
    
    
    odb = displayio.OnDiskBitmap('/RADARC_Logo.bmp')
    logo = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
    splash.y = 0
    splash.append(logo)
    
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


def create_menu():   
    for i, item in enumerate(menu_items):
        text_color = 0xFFFFFF if i == selected_index else 0xAAAAAA
 
        text_area= label.Label(terminalio.FONT, scale = 3, text=item, color=text_color, x=20, y=30 + i * 30)
        
        menu.append(text_area)
       
# Function to update the display
def update_menu():
    
    
    for i, item in enumerate(menu_items):
        menu[i].color = 0xFFFFFF if i == selected_index else 0xAAAAAA
        
        
#
display_splash()

while(switch_enc.value is True):
    time.sleep(0.1)
# Create menu display context
menu = displayio.Group()
display.root_group = menu        
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