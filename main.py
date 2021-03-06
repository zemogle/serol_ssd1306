import os.path
import time
import threading
import json

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
STATUS_FACE = { 'FAILED':"serolbw_fail.png",
                'CANCELED':"serolbw_fail.png",
                'WINDOW_EXPIRED' : "serolbw_fail.png",
                'COMPLETED' : "serolbw_thinking1.png",
                'PENDING'   : "serolbw_thinking6.png",
                }

SECRETS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),'secrets.json'))
THINKING = ['serolbw_thinking1.png','serolbw_thinking2.png','serolbw_thinking4.png','serolbw_thinking5.png','serolbw_thinking6.png','serolbw_thinking5.png','serolbw_thinking4.png','serolbw_thinking2.png']

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

fontpath = os.path.abspath(os.path.join(os.path.dirname(__file__),"fonts","Affogato-Regular.ttf"))

class Looping(object):

    def __init__(self):
     self.isRunning = True
     self.sequence = []
     for img in THINKING:
         img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"images", img))
         logo = Image.open(img_path).convert("RGBA")
         im = logo.resize(device.size)
         self.sequence.append(im)

    def runForever(self):
        i = 0
        size = len(THINKING)
        while self.isRunning == True:
            ia = i % size
            img = self.sequence[ia]
            device.display(img.convert(device.mode))
            i += 1
            time.sleep(0.05)

        return

def show_img(img):
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"images", img))
    logo = Image.open(img_path).convert("RGBA")
    im = logo.resize(device.size)
    device.display(im.convert(device.mode))
    time.sleep(4)
    return

def show_msg(text):
    font = ImageFont.truetype(fontpath, 16)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((5, 10), "{}".format(text), fill="white", font=font)
    time.sleep(4)
    return

def boot():
    font_lg = ImageFont.truetype(fontpath, 30)
    font_sm = ImageFont.truetype(fontpath, 12)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30, 10), "Welcome to..", fill="white")
    time.sleep(4)

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((35, 0), "Serol", fill="white", font=font_lg)
        draw.text((20, 32), "Cosmic Explorer", fill="white", font=font_sm)
    time.sleep(4)
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"images", 'serolscreenblack.png'))
    logo = Image.open(img_path).convert("RGBA")
    img = logo.resize(device.size)
    device.display(img.convert(device.mode))
    time.sleep(4)
    return


def import_settings():
    with open(SECRETS_FILE) as json_data:
        d = json.load(json_data)
    return d

def request_status(rid):
    settings = import_settings()
    headers = {'Authorization': 'Token {}'.format(settings['valhalla_token'])}
    resp = requests.get('https://observe.lco.global/api/userrequests/{}/'.format(rid), headers = headers)
    if resp.status_code not in [200, 201]:
        return 'ERROR'
    msg = resp.json()['state']
    return msg

def check_status():
    settings = import_settings()
    for rid in settings['request_ids']:
        show_msg("Checking {}".format(rid))
        l = Looping()
        t = threading.Thread(target = l.runForever)
        t.start()
        resp = request_status(rid)
        l.isRunning = False
        show_img(STATUS_FACE[resp])
        time.sleep(10)
    return


@click.command()
@click.option('--update', is_flag=True)
@click.option('--splash', is_flag=True)
def runner(update, splash):
    if update:
        check_status()
    if splash:
        boot()
    return


if __name__ == "__main__":
    try:
        runner()
    except KeyboardInterrupt:
        pass
