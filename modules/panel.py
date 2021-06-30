import time
import subprocess

import RPi.GPIO as GPIO

from util import gpio
from util import timer
from util.gpio import lights
from util.gpio import motion

from net import kunapi

gpio.setup()

lights.setup()
motion.setup()

motionTimer = timer.Timer()
noMotionTimer = timer.Timer()

def update():
	motionOn = False
	while True:
		motionDetected = GPIO.input(motion.MOTION_SENSOR_PIN)
		
		if motionDetected:
			if not motionOn:
				motionOn = True
				run('vcgencmd display_power 1', shell=True)
				lights.send_light()
				noMotionTimer.reset()
		else:
			if motionOn:
				motionOn = False
				motionTimer.reset()
				if noMotionTimer.getElapsedTime() > 120:
					run('vcgencmd display_power 0', shell=True)
					print("no motion for 10 seconds")

		time.sleep(3)
	return