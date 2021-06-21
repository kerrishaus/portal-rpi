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
		if GPIO.input(motion.MOTION_SENSOR_PIN):
			print("Motion Detected!")
		time.sleep(1)
	return