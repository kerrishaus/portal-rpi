import time
import os
import platform
import socket
import subprocess

from util import gpio
from util.gpio import lights
from util.gpio import motion
from util import timer
from util import config

from net import kunapi

VERSION = 1

print("Starting Portal Client v" + str(VERSION))

#config.load_config()

print("My name is " + config.my_name + ".")

gpio.setup()

lights.setup()
lights.fail_light()
lights.recv_light()
lights.send_light(1)

motion.setup()

payload = {
	"deviceid": config.api_device_id,
	"status": "1",
	"token": "NO-TOKEN"
}

x = kunapi.post("status", payload)
if x.status_code:
	lights.send_light()
else:
	print("failed to alert api of status: " + x.status_code)
	lights.fail_light()

s = socket.socket()
s.bind(("0.0.0.0", 27000))

if s.listen():
	lights.send_light()
else:
	lights.fail_light()

lights.send_light()

print("Portal Client is ready.")

def shutdown():
	x = kunapi.post("status", {"deviceid":"2","status":"0","token":"NO-TOKEN"})
	if x.status_code:
		lights.send_light()
	else:
		print("failed to notify api of change in status: " + x.status_code)
		lights.fail_light()
		
	lights.fail_light(3)
		
	gpio.cleanup()
	s.close()

def send_message(message):
	sent = csock.send(message.encode())
	if sent != 0:
		lights.send_light()
	else:
		lights.fail_light()
	return sent

api_timer = timer.Timer()

try:
	while True:
		#if api_timer.getElapsedTime() > 1:
		#	x = post_api("status", {"deviceid":"2","status":"1","token":"NO-TOKEN"})
		#	if x.status_code:
		#		send_light()
		#	else:
		#		print("failed to alert api of status: " + x.status_code)
		#		fail_light()
		#	api_timer.reset()

		csock, caddr = s.accept()
		print("/ ACCEPTED SOCKET")
		try:
			while True:
				data = csock.recv(1024)
				if data:
					lights.recv_light()

					data = data.decode()
					print("> " + data)
					if data == "SHUTDOWN":
						print("shutting down")
						if send_message("SHUTTING_DOWN"):
							os.system("poweroff")

					elif data == "REBOOT":
						if send_message("REBOOTING"):
							subprocess.Popen(['sudo', 'shutdown','-r','now'])

					elif data == "STOP":
						send_message("STOPPING")
						shutdown()
						break

					elif data == "TELL_HIM_HES_UGLY":
						print("You can't even do that righ!")
						send_message("YOU'RE CHUBBY")

					elif data == "DISCONNECT":
						if send_message("BYE_BYE"):
							csock.close()
							break

					elif data == "SET_NAME":
						send_message("OKAY_GIVE_NAME")

						data = csock.recv(1024)
						if data:
							new_name = data.decode()
							config.updateConfig("DEFAULT", "MyName", new_name)
							config.my_name = new_name
							print("my new name is " + config.my_name)
							send_message("NAME_SET")
						else:
							print("NO name given")
							send_message("FAIL_INVALID_DATA")

					else:
						if data == "GIVE_NAME":
							message = config.my_name
						elif data == "PLATFORM_INFO":
							message = os.name + " " + platform.system() + " " + platform.release()
						else:
							message = "UNKNOWN_COMMAND"

						send_message(message)
				else:
					print("Socket connected, but no data was received.")
					lights.fail_light()
		finally:
			print("\ CLOSING SOCKET")
			csock.close()
except KeyboardInterrupt:
	shutdown()
