# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_bmp581 import bmp581

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
bmp = bmp581.BMP581(i2c)

bmp.pressure_oversample_rate = bmp581.OSR16

while True:
    for pressure_oversample_rate in bmp581.pressure_oversample_rate_values:
        print(
            "Current Pressure oversample rate setting: ", bmp.pressure_oversample_rate
        )
        for _ in range(10):
            press = bmp.pressure
            print("pressure:{:.2f}kPa".format(press))
            time.sleep(0.5)
        bmp.pressure_oversample_rate = pressure_oversample_rate
