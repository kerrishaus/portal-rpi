import time

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
	while True:
		motionDetected = GPIO.input(motion.MOTION_SENSOR_PIN)
		if motionDetected:
			lights.send_light()
			noMotionTimer.reset()
		else:
			motionTimer.reset()
			if noMotionTimer.getElapsedTime() > 10:
				print("no motion in 10 seconds")
		time.sleep(1)
	return