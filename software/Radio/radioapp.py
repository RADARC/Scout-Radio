#import ssd1306
#import framebuf
#import mcp23017
import si4735_CP
#from machine import I2C, Pin
import time
import board
import busio
import sys
import os
import displayio
import terminalio
import rotaryio
from digitalio import DigitalInOut, Direction, Pull
from fourwire import FourWire
from adafruit_st7789 import ST7789
from adafruit_display_text import label
from analogio import AnalogIn

os.chdir("/Radio")

switch1 = DigitalInOut(board.GP2)
switch2 = DigitalInOut(board.GP3)
switch3 = DigitalInOut(board.GP6)
switch4 = DigitalInOut(board.GP7)
switch5 = DigitalInOut(board.GP21)
switch6 = DigitalInOut(board.GP22)
switch_Enc = DigitalInOut(board.GP9)
torch = DigitalInOut(board.GP16)

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

switch1.direction = Direction.INPUT
switch1.pull = Pull.UP
switch2.direction = Direction.INPUT
switch2.pull = Pull.UP
switch3.direction = Direction.INPUT
switch3.pull = Pull.UP
switch4.direction = Direction.INPUT
switch4.pull = Pull.UP
switch5.direction = Direction.INPUT
switch5.pull = Pull.UP
switch6.direction = Direction.INPUT
switch6.pull = Pull.UP
torch.direction = Direction.OUTPUT
torch.value = False

switch_Enc.direction = Direction.INPUT
switch_Enc.pull = Pull.UP

encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
last_position = 0

displayio.release_displays()

#tft_cs = board.GP9
tft_dc = board.GP8
spi_mosi = board.GP11
spi_clk = board.GP10


spi = busio.SPI(spi_clk, spi_mosi)


display_bus = FourWire(spi, command=tft_dc, polarity = 1, phase = 1, reset=board.GP12)

display = ST7789(display_bus, width=240, height=240,rowstart=80, rotation=90)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(240, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(200, 200, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group(scale=2, x=48, y=40)
text = "Starting up..."
text_status = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_status)  # Subgroup for text scaling
splash.append(text_group)

# Draw a label
text_group = displayio.Group(scale=3, x=48, y=80)
text = ""
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

text_group = displayio.Group(scale=2, x=48, y=100)
text = ""
text_station_name = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_station_name)  # Subgroup for text scaling
splash.append(text_group)


text_group = displayio.Group(scale=2, x=48, y=120)
text = ""
text_station_text = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_station_text)  # Subgroup for text scaling
splash.append(text_group)

text_group = displayio.Group(scale=2, x=28, y=140)
text = ""
text_signalstrength = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_signalstrength)  # Subgroup for text scaling
splash.append(text_group)



i2c = busio.I2C( board.GP19, board.GP18)

si4735_reset_pin = DigitalInOut(board.GP17)
si4735_reset_pin.direction = Direction.OUTPUT
radio = si4735_CP.SI4735(i2c, 0x63, si4735_reset_pin)

def displayFrequency():
    if radio.getMode() == si4735_CP.FM_CURRENT_MODE:
        text_area.text = "FM " + str(radio.getFrequency()/100)
                
    elif radio.getMode() == si4735_CP.SSB_CURRENT_MODE:
        text_area.text = "SSB " + str(radio.getFrequency()/1000)
        
    elif radio.getMode() == si4735_CP.AM_CURRENT_MODE:
        text_area.text = "AM " + str(radio.getFrequency())


radio.reset()
addr = radio.get_device_i2c_address()
if addr == 0:
    sys.exit()

radio.setFM()
radio.setRDSConfig(1,3,3,3,3)
radio.setFrequency(9703)
displayFrequency()
text_status.text = ""

oldvol=32 #int((1 - (pot0.value / 65535)) * 63)
radio.setVolume(oldvol)

#BM = bytearray(b'\xfc\x00\x03\xff\xbf\xfc\x00\x03\xf0\xfc\x00\x00\x7f\x6f\xe0\x00\x03\xf0\xff\xff\xf8\x1f\x6f\x81\xff\xff\xf0\xff\xff\xff\x0f\x5f\x0f\xff\xff\xf0\xff\xff\xff\x8f\x6f\x1f\xff\xff\xf0\xff\xff\xff\xc7\xee\x3f\xff\xff\xf0\xff\xff\xff\xc7\xfe\x3f\xff\xff\xf0\xff\xff\xff\xcf\xff\x3f\xff\xff\xf0\xff\xff\xff\x8f\xbf\x1f\xff\xff\xf0\xff\xff\xfe\x1f\x9f\x87\xff\xff\xf0\xff\xff\xe0\x3f\x5f\xc0\x7f\xff\xf0\xff\xe7\xe0\x7f\x0f\xe0\x7e\x7f\xf0\xff\xdb\xe0\x3f\x6f\xc0\x7d\xbf\xf0\xff\xbd\xfe\x1f\xff\x87\xfb\xdf\xf0\xff\xbd\xff\x8f\xff\x1f\xfb\xdf\xf0\xff\xbd\xff\xcf\xff\x3f\xfb\xdf\xf0\xff\x7e\xff\xc7\x4e\x3f\xf7\xef\xf0\xff\x7e\xff\xc7\x6e\x3f\xf7\xef\xf0\xff\x7e\xff\xcf\x6f\x3f\xf7\xef\xf0\xff\x7e\xff\x0f\x6f\x0f\xf7\xef\xf0\xff\x7e\xfc\x1f\x1f\x83\xf7\xef\xf0\xff\x7e\xc0\x7f\xff\xe0\x37\xef\xf0\xff\x7e\xe0\x7f\xff\xe0\x77\xef\xf0\x7f\x7f\xf8\x1f\xbf\x81\xff\xef\xe0\x7f\x7f\xff\x0f\x9f\x0f\xff\xef\xe0\x7f\x7f\xff\xcf\x5f\x3f\xff\xef\xe0\x7f\xff\xff\xc7\x0e\x3f\xff\xff\xe0\x7e\xff\xff\xc7\x6e\x3f\xff\xf7\xe0\x7e\xff\xff\xcf\xff\x3f\xff\xf7\xe0\xfe\xff\xff\x8f\xff\x1f\xff\xf7\xf0\xbe\xff\xfe\x1f\xff\x87\xff\xf7\xd0\xbe\xff\xe0\x3f\x0f\xc0\x7f\xf7\xd0\xbd\xff\xe0\x7f\x6f\xe0\x7f\xfb\xd0\xdd\xff\xe0\x3f\x1f\xc0\x7f\xfb\xb0\xeb\xff\xfe\x1f\x4f\x87\xff\xfd\x70\xff\xff\xff\x8f\x6f\x1f\xff\xff\xf0\xff\xff\xff\xcf\xff\x3f\xff\xff\xf0\xff\xff\xff\xc7\xfe\x3f\xff\xff\xf0\xff\xff\xff\xc7\x9e\x3f\xff\xff\xf0\xff\xff\xff\x8f\x6f\x1f\xff\xff\xf0\xff\xff\xff\x0f\x7f\x0f\xff\xff\xf0\xff\xff\xf8\x1f\x6f\x81\xff\xff\xf0\xfc\x00\x00\x7f\x2f\xe0\x00\x03\xf0\xfc\x00\x03\xff\xff\xfc\x00\x03\xf0')

#fb = framebuf.FrameBuffer(BM, 68, 44, framebuf.MONO_HLSB)
#display.fill(0)
#display.blit(fb, 30, 20)
#display.text('HF PA Controller',0,0,1)
#display.text(bands[0], 0, 8,1)
#display.fill_rect(82, 8, 20, 8,1)
#display.text('Rx', 84, 7, 0)
#display.show()

t=0
while True:
    
    newvol= 32 #int((1 - (pot0.value / 65535)) * 63)
    if newvol!=oldvol:
        oldvol=newvol
        radio.setVolume(newvol)
        print(newvol)
 

    time.sleep(0.050)
    
    position = encoder.position
    if last_position is None or position != last_position:
        
        if radio.getMode() == si4735_CP.FM_CURRENT_MODE:
            increment=10
        elif radio.getMode() == si4735_CP.SSB_CURRENT_MODE:
            increment=1
        elif radio.getMode() == si4735_CP.AM_CURRENT_MODE:
            increment=1
            
        if position > last_position:
            radio.setFrequency(radio.getFrequency()+increment)
           
        elif position < last_position:
            radio.setFrequency(radio.getFrequency()-increment)
           
        displayFrequency()
            
    last_position = position
    
    if switch1.value is False:
            #Bandwidth, only for SSB
            if radio.getMode() == si4735_CP.SSB_CURRENT_MODE:
                oldBW = radio.getSSBbandwidth()
                
                if (oldBW == 5):
                    radio.setSSBAudioBandwidth(0)
                else:
                    radio.setSSBAudioBandwidth(oldBW+1)
                
         
            
    #Mode button
    if switch5.value is False:
        
        
        
        
        if radio.getMode() == si4735_CP.FM_CURRENT_MODE:
            #Go to AM Mode
            radio.setAM()
            radio.setFrequency(198)
            
       
        elif radio.getMode() == si4735_CP.AM_CURRENT_MODE:
           
            #Go to SSB Mode
            text_status.text = "Please wait..."
            radio.powerDown()
            radio.patchPowerUp()
            radio.downloadPatch()

            radio.setSSB(si4735_CP.SSB_SIDEBAND_USB)
            radio.setFrequency(14000)

            radio.setSSBConfig(1, 0, 0, 1, 0, 1)
            text_status.text = ""
            
        elif radio.getMode() == si4735_CP.SSB_CURRENT_MODE:
            
            #If volume button is down when the mode button is pressed and mode is SSB
            #Switch LSB/USB
            if switch4.value is False:
                if radio.getSSBsideband() == si4735_CP.SSB_SIDEBAND_LSB:
                     radio.setSSB(si4735_CP.SSB_SIDEBAND_USB)
                     radio.setFrequency(radio.getFrequency())
                elif radio.getSSBsideband() == si4735_CP.SSB_SIDEBAND_USB:
                     radio.setSSB(si4735_CP.SSB_SIDEBAND_LSB)
                     radio.setFrequency(radio.getFrequency())
                
            else:
        
                #Go to FM Mode
                radio.setFM()
                radio.setRDSConfig(1,3,3,3,3)
                radio.setFrequency(9703)
            
            
        displayFrequency()
        
   
   
    if time.time()-t > 1:
        
        sigquality = radio.getCurrentReceivedSignalQuality(0)
        
        text_signalstrength.text = "rssi:" + str(sigquality["rssi"]) + " SNR:" + str(sigquality["SNR"])
      
        if radio.getMode() == si4735_CP.FM_CURRENT_MODE:
            radio.getRDSStatus(0,0,0)
          
            text_station_name.text = radio.station_name
            text_station_text.text = radio.station_text
        
        t= time.time()
