import time

import RPi.GPIO as GPIO

from util import gpio
from util.gpio import lights
from util.gpio import motion

from net import kunapi

gpio.setup()

motion.setup()

def update():
	while True:
		motionDetected = GPIO.input(motion.MOTION_SENSOR_PIN)
		if motionDetected:
			print("Motion Detected!")
		time.sleep(.5)
	return