import RPi.GPIO as GPIO

print("A module from the util/gpio package was imported.")

def setup():
	GPIO.cleanup() # Always want to use a clean GPIO header.
	GPIO.setmode(GPIO.BCM)
	print("GPIO module is ready.")

def cleanup():
	GPIO.cleanup()
	print("GPIO module cleaned up.")