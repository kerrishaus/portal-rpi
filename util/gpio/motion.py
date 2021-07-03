import time
import subprocess

import RPi.GPIO as GPIO

from util import timer
from util import config
from net import kunapi

MOTION_SENSOR_PIN = 14

#in seconds
MAX_IDLE_TIME = 360

motion = False

def setup():
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

def display_power_on():
    return subprocess.run('vcgencmd display_power 1', shell=True)

def display_power_off():
    return subprocess.run('vcgencmd display_power 0', shell=True)

def is_display_powered():
    # ask if the display is already powered on
    result = subprocess.run('vcgencmd display_power -1', shell=True, capture_output=True)
    output = str(result.stdout)
    if str(output) != "b'display_power=1\\n'":
        return True
    else:
        return False

def update():
    global motion

    if GPIO.input(MOTION_SENSOR_PIN):
        if not motion:
            motion = True
            print("motion detected")

            if is_display_powered():
                print("powering on display")
                display_power_on()
                # wake up screen if it's blanked
                subprocess.run('export DISPLAY=:0 && xset s reset', shell=True)
                print("display is already on")

            kunapi.status(3)
    else:
        if motion:
            motion = False
            print("motion no longer detected")
            kunapi.status(4)
        elif not motion and not is_display_powered():
            # get idle time from xserver in ms
            result = subprocess.run('export DISPLAY=:0 && sudo -u pi xprintidle', shell=True, capture_output=True)
            output = str(result.stdout)
            output = output[2:len(output) - 3]
            idletime = int(output)
            if idletime > (MAX_IDLE_TIME * 1000):
                display_power_off()
    return