# this module requires vcgencmd to control the monitor.

import RPi.GPIO as GPIO
from gpiozero import DigitalInputDevice

import subprocess

from util import timer
from util import config
from util import display
from net import kerrishausapi

MOTION_SENSOR_PIN = 17

motion = False
motion_radar = DigitalInputDevice(MOTION_SENSOR_PIN, pull_up=False, bounce_time=5)

def setup():
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)
    print("Radar motion module ready")

def motion_start():
    global motion
    
    if not motion:
        motion = True
        print("motion detected by radar")
        kerrishausapi.status(4)
        
        # reset xserver idle time
        subprocess.run("export DISPLAY=:0 && xset s reset", shell=True, capture_output=True)

def motion_stop():
    global motion
    
    if motion:
        motion = False
        print("motion no longer detected by radar")
        kerrishausapi.status(5)
    
def update():
    global motion
    global motion_radar
    
    motion_radar.when_activated = motion_start
    motion_radar.when_deactivated = motion_stop