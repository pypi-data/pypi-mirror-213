# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_adt7410 import adt7410

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
adt = adt7410.ADT7410(i2c)

adt.operation_mode = adt7410.SPS

while True:
    for operation_mode in adt7410.operation_mode_values:
        print("Current Operation mode setting: ", adt.operation_mode)
        for _ in range(10):
            print("Temperature: {:.2f}C".format(adt.temperature))
            time.sleep(0.5)
        adt.operation_mode = operation_mode
