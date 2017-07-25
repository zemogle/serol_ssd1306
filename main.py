#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display the Serol head while booting.
"""

import os.path
import time

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306


serial = i2c(port=1, address=0x3C)

device = ssd1306(serial)

from PIL import Image


def main():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'serolheadgrey.png'))
    logo = Image.open(img_path).convert("RGBA")
    img = logo.resize(device.size)
    device.display(img.convert(device.mode))
    time.sleep(20)
    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
