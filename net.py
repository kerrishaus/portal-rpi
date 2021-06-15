import RPi.GPIO as GPIO
import time
import os
import platform
import socket
import subprocess
import requests

VERSION = 1

print("Starting Portal Client v" + str(VERSION))

FAIL_LED_PIN = 17
RECV_LED_PIN = 27
SEND_LED_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(RECV_LED_PIN, GPIO.OUT)
GPIO.setup(SEND_LED_PIN, GPIO.OUT)
GPIO.setup(FAIL_LED_PIN, GPIO.OUT)

light_duration = .08

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

fail_light()
recv_light()
send_light(1)

def post_api(endpoint, payload):
	r = requests.post("https://api.kunindustries.com/portal/devices/" + endpoint + ".php", data = payload)
	send_light()
	return r

payload = {
	"deviceid": "2",
	"status": "1",
	"token": "NO-TOKEN"
}

x = post_api("status", payload)
if x.status_code:
	send_light()
else:
	print("failed to alert api of status: " + x.status_code)
	fail_light()

s = socket.socket()
if s.bind(("0.0.0.0", 27000)):
	send_light()
else:
	fail_light()

if s.listen():
	send_light()
else:
	fail_light()

send_light()

my_name = "Raspberry Pi"

def shutdown():
	x = post_api("status", {"deviceid":"2","status":"0","token":"NO-TOKEN"})
	if x.status_code:
		send_light()
	else:
		print("failed to alert api of status: " + x.status_code)
		fail_light()
		
	fail_light()
	fail_light()
	fail_light()
		
	GPIO.cleanup()
	s.close()

class Timer:
	start_time = time.monotonic()

	def getElapsedTime():
		return time.monotonic() - start_time

	def reset():
		last_time = getElapsedTime()
		start_time = time.monotonic()
		return last_time

api_timer = Timer()

try:
	while True:
		if api_timer.getElapsedTime() > 1:
			x = post_api("status", {"deviceid":"2","status":"1","token":"NO-TOKEN"})
			if x.status_code:
				send_light()
			else:
				print("failed to alert api of status: " + x.status_code)
				fail_light()
			api_timer.reset()

		csock, caddr = s.accept()
		data = csock.recv(1024)
		if data:
			recv_light()

			data = data.decode()
			print(data)
			if data == "SHUTDOWN":
				print("shutting down")
				message = "SHUTTING_DOWN"
				sock_stat = csock.send(message.encode())
				if sock_stat != 0:
					send_light()
					os.system("poweroff")
				else:
					message = "FAIL"
					csock.send(message.encode())
					fail_light()
			if data == "TELL_HIM_HES_UGLY":
				print("You can't even do that righ!")
				message = "YOU'RE CHUBBY!"
				sock_stat = csock.send(message.encode())
				if sock_stat != 0:
					send_light()
					os.system("poweroff")
				else:
					message = "FAIL"
					csock.send(message.encode())
					fail_light()
			elif data == "REBOOT":
				message = "REBOOTING"
				sock_stat = csock.send(message.encode())
				if sock_stat != 0:
					send_light()
					subprocess.Popen(['sudo', 'shutdown','-r','now'])
				else:
					message = "FAIL"
					csock.send(message.encode())
					fail_light()
			elif data == "STOP":
				message = "STOPPING"
				sock_stat = csock.send(message.encode())
				if sock_stat != 0:
					send_light()
				else:
					message = "FAIL"
					csock.send(message.encode())
					fail_light()
					
				shutdown()
				break
			elif data == "GIVE_NAME":
				message = my_name
			elif data == "PLATFORM_INFO":
				message = os.name + " " + platform.system() + " " + platform.release()
			else:
				message = "UNKNOWN_COMMAND"

			sent_bytes = csock.send(message.encode())

			if sent_bytes != 0:
				send_light()
			else:
				fail_light()
		else:
			fail_light()

		csock.close()
except KeyboardInterrupt:
	shutdown()