# SPDX-FileCopyrightText: 2024 Tim Cocks for Adafruit Industries

# SPDX-FileCopyrightText: 2024 Jose D. Montoya

#

# SPDX-License-Identifier: MIT


import time
import board
import gc
from fourwire import FourWire
from adafruit_st7789 import ST7789
from adafruit_display_text.bitmap_label import Label
from terminalio import FONT
from displayio import Group, release_displays
from busio import SPI, I2C
import adafruit_lsm303dlh_mag
import adafruit_lsm303_accel
from digitalio import DigitalInOut, Direction, Pull
import supervisor
from math import atan2, degrees


def vector_2_degrees(x, y):
    angle = degrees(atan2(y, -x))
    if angle < 0:
        angle += 360
    return angle
                         


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


spi = SPI(spi_clk, spi_mosi)


display_bus = FourWire(spi, command=tft_dc, polarity = 1, phase = 1, reset=board.GP12)

display = ST7789(display_bus, width=240, height=240,rowstart=80, rotation=90)


# create a main_group to hold anything we want to show on the display.
# Make the display context
main_group = Group()
display.root_group = main_group


# Initialize I2C bus and sensor.


i2c = I2C(board.GP5, board.GP4)

mag_sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
acc_sensor = adafruit_lsm303_accel.LSM303_Accel(i2c)

# Create Label(s) to show the readings. If you have a very small

# display you may need to change to scale=1.

bearing_label = Label(FONT, text="", scale=2)
angle_xy_label = Label(FONT, text="", scale=2)
angle_xz_label = Label(FONT, text="", scale=2)
angle_yz_label = Label(FONT, text="", scale=2)

# place the label(s) 

bearing_label.anchor_point = (0, 0,)
bearing_label.anchored_position = (0,0,)
angle_xy_label.anchor_point = (0, 0,)
angle_xy_label.anchored_position = (0,40,)
angle_xz_label.anchor_point = (0, 0)
angle_xz_label.anchored_position = (0,80,)
angle_yz_label.anchor_point = (0, 0)
angle_yz_label.anchored_position = (0,120,)


# add the label(s) to the main_group

main_group.append(bearing_label)
main_group.append(angle_xy_label)
main_group.append(angle_xz_label)
main_group.append(angle_yz_label)



# bias correction values unique to device
bias_mag_x = -70.7272
bias_mag_y = 50.6818
bias_mag_z = 17.2449

bias_acc_x = -0.554567
bias_acc_y = 0.0382462
bias_acc_z = -1.85493

def get_heading(_mag_sensor):
    magnet_x, magnet_y, _ = _mag_sensor.magnetic
    corrected_magnet_x = magnet_x - bias_mag_x
    corrected_magnet_y = magnet_y - bias_mag_y
    return vector_2_degrees(corrected_magnet_x, corrected_magnet_y)

def get_anglexy( _acc_sensor):
    acc_x, acc_y, acc_z = acc_sensor.acceleration
    corrected_acc_x = acc_x - bias_acc_x
    corrected_acc_y = acc_y - bias_acc_y
    corrected_acc_z = acc_z - bias_acc_z
    return vector_2_degrees(corrected_acc_x, corrected_acc_y)

def get_anglexz( _acc_sensor):
    acc_x, acc_y, acc_z = acc_sensor.acceleration
    corrected_acc_x = acc_x - bias_acc_x
    corrected_acc_y = acc_y - bias_acc_y
    corrected_acc_z = acc_z - bias_acc_z
    return vector_2_degrees(corrected_acc_x, corrected_acc_z)

def get_angleyz( _acc_sensor):
    acc_x, acc_y, acc_z = acc_sensor.acceleration
    corrected_acc_x = acc_x - bias_acc_x
    corrected_acc_y = acc_y - bias_acc_y
    corrected_acc_z = acc_z - bias_acc_z
    return vector_2_degrees(corrected_acc_y, corrected_acc_z)
# begin main loop

while True:

    # update the text of the label(s) to show the sensor readings


    bearing_label.text = f"Bearing:{get_heading(mag_sensor):5.2f} deg"
    angle_xy_label.text = f"Angle XY:{get_anglexy(acc_sensor):5.2f} deg"
    angle_xz_label.text = f"Angle XZ:{get_anglexz(acc_sensor):5.2f} deg"
    angle_yz_label.text = f"Angle YZ:{get_angleyz(acc_sensor):5.2f} deg"
    
# check memory usage
    gc.collect() 
    print( "Available memory: {} bytes".format(gc.mem_free()) )

    if switch_enc.value is False:
        print ("ENCODER")
        supervisor.set_next_code_file('prog_mgr.py')
        supervisor.reload()

# wait for a bit
 
    time.sleep(0.5)