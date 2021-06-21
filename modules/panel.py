import time

from RPi.GPIO import GPIO

from util.gpio import lights
from util.gpio import motion
from net import kunapi

def update():
	while True:
		if GPIO.input(motion.MOTION_SENSOR_PIN):
			print("Motion Detected!")
		time.sleep(1)
	return