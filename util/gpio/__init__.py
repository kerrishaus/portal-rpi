import RPi.GPIO as GPIO

print("A module from the util/gpio package was imported.")

def setup():
	GPIO.setmode(GPIO.BCM)
	print("GPIO Module is ready.")

def cleanup():
	GPIO.cleanup()
	print("Cleaned up.")