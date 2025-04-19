# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display accelerometer data once per second """

import time
import board
import busio

import adafruit_lsm303_accel

i2c = busio.I2C(board.GP5, board.GP4)
bias_acc_x = -0.554567
bias_acc_y = 0.0382462
bias_acc_z = -1.85493

sensor = adafruit_lsm303_accel.LSM303_Accel(i2c)

while True:
    acc_x, acc_y, acc_z = sensor.acceleration
    corrected_acc_x = acc_x - bias_acc_x
    corrected_acc_y = acc_y - bias_acc_y
    corrected_acc_z = acc_z - bias_acc_z
    
    print("Acceleration (m/s^2): ({0:10.3f}, {1:10.3f}, {2:10.3f})".format(
            corrected_acc_x, corrected_acc_y, corrected_acc_z )  )
    print("")
    time.sleep(1.0)
