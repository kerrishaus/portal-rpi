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
    print("PassiveIR module is ready.")

def update():
    global motion

    # if motion is detected this tick
    if GPIO.input(MOTION_SENSOR_PIN):
        # reset user inactivity timer
        subprocess.run('export DISPLAY=:0 && sudo -u pi xset s reset', shell=True, capture_output=True)
        
        # don't do anything if motion has already been detected
        if not motion:
            motion = True
            print("motion detected by passiveir")

            if not display.is_display_powered():
                display.display_power_on()
                kerrishausapi.status(4)

        return
    
    # motion not detected this tick
    if motion:
        motion = False
        print("motion no longer detected by passiveir")

    # FIXME: it's possible that is_display_powered here is always returning true
    # and causing us to attempt to power off the display over and over
    if not motion and display.is_display_powered():
        idleTime = display.get_idle_time()
        
        if idleTime > (config.screen_idle_time * 1000):
            print("idle time limit reached and display is powered on, passiveir is powering off display", str(idleTime))
            display.display_power_off()
            kerrishausapi.status(5)