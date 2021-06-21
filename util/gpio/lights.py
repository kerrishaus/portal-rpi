import RPi.GPIO as GPIO
import time

FAIL_LED_PIN = 17
RECV_LED_PIN = 27
SEND_LED_PIN = 22

light_duration = .08

def setup():
    GPIO.setup(RECV_LED_PIN, GPIO.OUT)
    GPIO.setup(SEND_LED_PIN, GPIO.OUT)
    GPIO.setup(FAIL_LED_PIN, GPIO.OUT)

def send_light(duration = light_duration):
	GPIO.output(SEND_LED_PIN, GPIO.HIGH)
	time.sleep(duration)
	GPIO.output(SEND_LED_PIN, GPIO.LOW)

def recv_light(duration = light_duration):
	GPIO.output(RECV_LED_PIN, GPIO.HIGH)
	time.sleep(duration)
	GPIO.output(RECV_LED_PIN, GPIO.LOW)

def fail_light(duration = light_duration):
	GPIO.output(FAIL_LED_PIN, GPIO.HIGH)
	time.sleep(duration)
	GPIO.output(FAIL_LED_PIN, GPIO.LOW)