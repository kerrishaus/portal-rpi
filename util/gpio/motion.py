import time
import subprocess

import RPi.GPIO as GPIO

from util import timer
from util import config
from net import kunapi

MOTION_SENSOR_PIN = 14

motion = False

def setup():
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

def update():
    global motion

    if GPIO.input(MOTION_SENSOR_PIN):
        if not motion:
            motion = True
            result = subprocess.run('vcgencmd display_power -1', shell=True, capture_output=True)
            output = result.stdout
            if str(output) == "display_power=0":
                subprocess.run('vcgencmd display_power 1', shell=True, capture_output=True)
            else:
                print("display is already on")
            kunapi.status(3)
    else:
        if motion:
            motion = False
            kunapi.status(4)
            # dont know if i want to do this just yet
            #subprocess.run('vcgencmd display_power 0', shell=True)
    return