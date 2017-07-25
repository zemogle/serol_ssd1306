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

from PIL import Image, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.virtual import viewport
from luma.core.render import canvas

serial = i2c(port=1, address=0x3C)

device = ssd1306(serial)


def boot():
    font_lg = ImageFont.truetype("Affogato-Regular.ttf", 30)
    font = ImageFont.truetype("Affogato-Regular.ttf", 12)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30, 10), "Welcome to..", fill="white")
    time.sleep(4)

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((35, 0), "Serol", fill="white", font=font_lg)
        draw.text((10, 32), "Cosmic Explorer", fill="white", font=font)
    time.sleep(4)
    return

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
        boot()
        main()
    except KeyboardInterrupt:
        pass
