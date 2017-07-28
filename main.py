import os.path
import time
import threading

import click
from PIL import Image, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.virtual import viewport
from luma.core.render import canvas
import requests

URL_BASE = 'http://10.73.224.41:5000'
URL_MISSION = '{}/mission/'.format(URL_BASE)
URL_CHALLENGE = '{}/challenge/'.format(URL_BASE)
URL_STATUS = '{}/'.format(URL_BASE)
RESPONSES = {'ok' : "tick.png", ""}
SECRETS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),'secrets.json'))
THINKING = ['serolbw_thinking1.png','serolbw_thinking2.png','serolbw_thinking4.png','serolbw_thinking5.png','serolbw_thinking6.png']

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

class Looping(object):

    def __init__(self):
     self.isRunning = True

    def runForever(self):
       while self.isRunning == True:
          img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"images", 'serolheadblack.png'))
          logo = Image.open(img_path).convert("RGBA")
          img = logo.resize(device.size)
          device.display(img.convert(device.mode))
          #time.sleep(0.1)

def boot():
    fontpath = os.path.abspath(os.path.join(os.path.dirname(__file__),"fonts","Affogato-Regular.ttf"))
    font_lg = ImageFont.truetype(fontpath, 30)
    font = ImageFont.truetype(fontpath, 12)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30, 10), "Welcome to..", fill="white")
    time.sleep(4)

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((35, 0), "Serol", fill="white", font=font_lg)
        draw.text((20, 32), "Cosmic Explorer", fill="white", font=font)
    time.sleep(4)
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"images", 'serolheadblack.png'))
    logo = Image.open(img_path).convert("RGBA")
    img = logo.resize(device.size)
    device.display(img.convert(device.mode))
    time.sleep(4)
    return


def import_settings():
    with open(SECRETS_FILE) as json_data:
        d = json.load(json_data)
    return d

def request_status(settings,):
    resp = requests.get('https://observe.lco.global/api/userrequests/3456/', headers = )

def check_status():
    resp = requests.get(URL_STATUS).json()
    if resp['status'] == 'ok':
        send_message("tick.png")
    time.sleep(10)

def send_message(img,colour=(0,255,0)):
    sense = SenseHat()
    sense.set_rotation(180)
    sense.load_image(img)


if __name__ == "__main__":
    try:
        boot()
    except KeyboardInterrupt:
        pass
