
import RPi.GPIO as GPIO

import subprocess

from util import timer
from util import config
from util import display
from net import kerrishausapi

MOTION_SENSOR_PIN = 17

motion = False

def setup():
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

def update():
    global motion

    if GPIO.input(MOTION_SENSOR_PIN):
        subprocess.run('export DISPLAY=:0 && sudo -u pi xset s reset', shell=True, capture_output=True)
        
        if not motion:
            motion = True
            print("motion detected")

            if not display.is_display_powered():
                display.display_power_on()
                kerrishausapi.status(4)
    else:
        if motion:
            motion = False
            print("motion no longer detected")
        elif not motion and display.is_display_powered():
            idleTime = display.get_idle_time()
            
            if idleTime > (config.screen_idle_time * 1000):
                print(str(idleTime))
                display.display_power_off()
                kerrishausapi.status(5)
    return
