
import RPi.GPIO as GPIO
from gpiozero import DigitalInputDevice

import subprocess

from util import timer
from util import config
from util import display
from net import kerrishausapi

MOTION_SENSOR_PIN = 17

motion = False
motion_radar = DigitalInputDevice(MOTION_SENSOR_PIN, pull_up=False)

def setup():
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

def motion_start():
    global motion
    
    if not motion:
        motion = True
        print("motion detected")
        kerrishausapi.status(4)
        
        subprocess.run("export DISPLAY=:0 && sudo -u pi xset s reset", shell=True, capture_output=True) # reset xserver idle time
        
        if not display.is_display_powered():
            display.display_power_on()

def motion_stop():
    global motion
    
    if motion:
        motion = False
        print("motion no longer detected")
        kerrishausapi.status(5)
    
def update():
    global motion
    global motion_radar
    
    motion_radar.when_activated = motion_start
    motion_radar.when_deactivated = motion_stop

    if not motion and display.is_display_powered():
        if display.get_idle_time() > (config.screen_idle_time * 1000):
            display.display_power_off()

    return
