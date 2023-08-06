# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_bmp581 import bmp581

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
bmp = bmp581.BMP581(i2c)

bmp.temperature_oversample_rate = bmp581.OSR4

while True:
    for temperature_oversample_rate in bmp581.temperature_oversample_rate_values:
        print(
            "Current Temperature oversample rate setting: ",
            bmp.temperature_oversample_rate,
        )
        for _ in range(10):
            temp = bmp.temperature
            print("temperature:{:.2f}C".format(temp))
            time.sleep(0.5)
        bmp.temperature_oversample_rate = temperature_oversample_rate
