# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display magnetometer data once per second """

import time
import board
import busio
import adafruit_lsm303dlh_mag

i2c = busio.I2C(board.GP5, board.GP4)
sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

# bias correction values unique to device
bias_mag_x = -70.7272
bias_mag_y = 50.6818
bias_mag_z = 17.2449


while True:
    mag_x, mag_y, mag_z = sensor.magnetic
    corrected_mag_x = mag_x - bias_mag_x
    corrected_mag_y = mag_y - bias_mag_y
    corrected_mag_z = mag_z - bias_mag_z
    print(
        "Magnetometer (gauss): ({0:10.3f}, {1:10.3f}, {2:10.3f})".format(
            corrected_mag_x, corrected_mag_y, corrected_mag_z
        )
    )
    print("")
    time.sleep(1.0)
