import time
import board
import busio
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag

i2c = busio.I2C(board.GP5, board.GP4)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

# Calibration:
accel_min_x = 10000
accel_max_x = -10000
accel_min_y = 10000
accel_max_y = -10000
accel_min_z = 10000
accel_max_z = -10000

mag_min_x = 10000
mag_max_x = -10000
mag_min_y = 10000
mag_max_y = -10000
mag_min_z = 10000
mag_max_z = -10000

# Record min/max values while rotating the sensor
print("Rotate the sensor...")
for _ in range(1000):  # Take many readings
    accel_x, accel_y, accel_z = accel.acceleration
    mag_x, mag_y, mag_z = mag.magnetic
    
    # Update min/max values
    accel_min_x = min(accel_min_x, accel_x)
    accel_max_x = max(accel_max_x, accel_x)
    accel_min_y = min(accel_min_y, accel_y)
    accel_max_y = max(accel_max_y, accel_y)
    accel_min_z = min(accel_min_z, accel_z)
    accel_max_z = max(accel_max_z, accel_z)

    # Update min/max values
    mag_min_x = min(mag_min_x, mag_x)
    mag_max_x = max(mag_max_x, mag_x)
    mag_min_y = min(mag_min_y, mag_y)
    mag_max_y = max(mag_max_y, mag_y)
    mag_min_z = min(mag_min_z, mag_z)
    mag_max_z = max(mag_max_z, mag_z)

    time.sleep(0.01) # Delay to allow readings

print("Calibration complete.")
print(f"Accelerometer X: Min={accel_min_x}, Max={accel_max_x}, Bias={(accel_max_x +accel_min_x)/2}")
print(f"Accelerometer Y: Min={accel_min_y}, Max={accel_max_y}, Bias={(accel_max_y +accel_min_y)/2}")
print(f"Accelerometer Z: Min={accel_min_z}, Max={accel_max_z}, Bias={(accel_max_z +accel_min_z)/2}")
print(f"Magnetometer X: Min={mag_min_x}, Max={mag_max_x}, Bias={(mag_max_x +mag_min_x)/2}")
print(f"Magnetometer Y: Min={mag_min_y}, Max={mag_max_y}, Bias={(mag_max_y +mag_min_y)/2}")
print(f"Magnetometer Z: Min={mag_min_z}, Max={mag_max_z}, Bias={(mag_max_z +mag_min_z)/2}")