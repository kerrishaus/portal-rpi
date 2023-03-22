import RPi.GPIO as GPIO

def setup():
	GPIO.setmode(GPIO.BCM)
	print("GPIO Module is ready.")

def cleanup():
	GPIO.cleanup()
	print("Cleaned up.")