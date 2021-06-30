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
            print("motion detected")

            # ask if the display is already powered on
            result = subprocess.run('vcgencmd display_power -1', shell=True, capture_output=True)
            output = result.stdout

            # if the display is not powered on
            if str(output) != "b'display_power=1\\n'":
                print("powering on display")
                subprocess.run('vcgencmd display_power 1', shell=True) # power it on
            else: # don't do anything, it's already on
                print("display is already on (" + str(output) + ")")
            kunapi.status(3)
    else:
        if motion:
            motion = False
            print("motion no longer detected")
            kunapi.status(4)
            # dont know if i want to do this just yet
            #subprocess.run('vcgencmd display_power 0', shell=True)
    return