import RPi.GPIO as GPIO

MOTION_SENSOR_PIN = 23

def setup():
    GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)