import RPi.GPIO as GPIO

def setup():
	GPIO.setmode(GPIO.BCM)

def cleanup():
	GPIO.cleanup()