# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display magnetometer data once per second """

import time
import board
import busio
import adafruit_lsm303dlh_mag

i2c = busio.I2C(board.GP5, board.GP4)
sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

while True:
    mag_x, mag_y, mag_z = sensor.magnetic

    print(
        "Magnetometer (gauss): ({0:10.3f}, {1:10.3f}, {2:10.3f})".format(
            mag_x, mag_y, mag_z
        )
    )
    print("")
    time.sleep(1.0)
