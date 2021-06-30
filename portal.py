import time
import os
import platform
import subprocess
import socket

from util import gpio
from util.gpio import lights
from util import timer
from util import config

from net import listen
from net import kunapi

VERSION = 1

print("Starting Portal Client " + str(VERSION))

# config is currently autoloaded
#config.load_config()

print("My name is " + config.my_name + ".")
print("I am device " + config.api_device_id)
print("My purpose is " + config.my_purpose)

gpio.setup()
lights.setup()
listen.setup()

if not kunapi.status(1):
	print("failed to alert api of status")

lights.send_light()

print("Portal Client is ready.")

if config.my_purpose == "Motion":
	from util.gpio import motion
	motion.setup()

def shutdown():
	if not kunapi.status(0):
		print("failed to notify api of change in status")
		lights.fail_light()
		
	lights.fail_light(3)
		
	gpio.cleanup()
	listen.s.close()

def send_message(message):
	sent = csock.send(message.encode())
	if sent != 0:
		lights.send_light()
	else:
		lights.fail_light()
	return sent

api_timer = timer.Timer()
light_timer = timer.Timer()

try:
	running = True
	while running: # this is the socket accept loop
		if api_timer.getElapsedTime() > config.api_status_interval:
			kunapi.status(1)
			api_timer.reset()

		if config.my_purpose == "Motion":
			motion.update()

		try:
			csock, caddr = listen.s.accept()
			csock.settimeout(.1)
			print("/ ACCEPTED SOCKET")
			try: # this is the client communication loop
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

						elif data == "SET_API_INTERVAL":
							send_message("OKAY_GIVE_INTERVAL")

							data = csock.recv(1024)
							if data:
								new_interval = data.decode()
								config.updateConfig("KUNINDUSTRIES_API", "StatusInterval", new_interval)
								config.api_status_interval = new_interval
								print("Status interval set to " + config.api_status_interval)
								send_message("INTERVAL_SET")
							else:
								print("Data is invalid.")
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
						print("Data received, but data was invalid.")
						lights.fail_light()
			except socket.timeout:
				print("socket timeout")
			finally:
				print("\ CLOSING SOCKET")
				csock.close()
		except socket.timeout:
			continue
except KeyboardInterrupt:
	shutdown()
	exit()

shutdown()