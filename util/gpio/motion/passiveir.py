import RPi.GPIO as GPIO

import subprocess

from util import config
from util import display
from net import kerrishausapi

MOTION_SENSOR_PIN = 17

motion = False

def setup():
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)
    print("PassiveIR motion module is ready.")

def update():
    global motion

    # if motion is detected this tick
    if GPIO.input(MOTION_SENSOR_PIN):
        # reset user inactivity timer
        subprocess.run('export DISPLAY=:0 && xset s reset', shell=True, capture_output=True)
        
        # don't do anything if motion has already been detected
        if not motion:
            motion = True
            print("motion detected by passiveir")
            kerrishausapi.status(4)

        return
    
    # motion not detected this tick
    if motion:
        motion = False
        print("motion no longer detected by passiveir")