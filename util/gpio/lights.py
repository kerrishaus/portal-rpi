import RPi.GPIO as GPIO
import time

from .. import config

FAIL_LED_PIN = 13
RECV_LED_PIN = 6
SEND_LED_PIN = 5

def setup():
    GPIO.setup(RECV_LED_PIN, GPIO.OUT)
    GPIO.setup(SEND_LED_PIN, GPIO.OUT)
    GPIO.setup(FAIL_LED_PIN, GPIO.OUT)
    print("Lights modules set up.")

def send_light(duration = config.debug_light_duration):
	GPIO.output(SEND_LED_PIN, GPIO.HIGH)
	time.sleep(duration)
	GPIO.output(SEND_LED_PIN, GPIO.LOW)

def recv_light(duration = config.debug_light_duration):
	GPIO.output(RECV_LED_PIN, GPIO.HIGH)
	time.sleep(duration)
	GPIO.output(RECV_LED_PIN, GPIO.LOW)

def fail_light(duration = config.debug_light_duration):
	GPIO.output(FAIL_LED_PIN, GPIO.HIGH)
	time.sleep(duration)
	GPIO.output(FAIL_LED_PIN, GPIO.LOW)
