import time
import os
import platform
import socket
import subprocess

from util import lights
from util import timer

from net import kunapi
from net import net
from net import sockets

VERSION = 1

print("Starting Portal Client v" + str(VERSION))

lights.setup()

lights.fail_light()
lights.recv_light()
lights.send_light(1)

payload = {
	"deviceid": "2",
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

my_name = "Raspberry Pi"

def shutdown():
	x = kunapi.post("status", {"deviceid":"2","status":"0","token":"NO-TOKEN"})
	if x.status_code:
		lights.send_light()
	else:
		print("failed to notify api of change in status: " + x.status_code)
		lights.fail_light()
		
	lights.fail_light()
	lights.fail_light()
	lights.fail_light()
		
	lights.cleanup()
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
		print("ACCEPTED SOCKET")
		try:
			while True:
				data = csock.recv(1024)
				if data:
					lights.recv_light()

					data = data.decode()
					print(data)
					if data == "SHUTDOWN":
						print("shutting down")
						message = "SHUTTING_DOWN"
						if send_message(message):
							os.system("poweroff")

					elif data == "TELL_HIM_HES_UGLY":
						print("You can't even do that righ!")
						message = "YOU'RE CHUBBY!"
						send_message(message)

					elif data == "DISCONNECT":
						message = "BYE"
						if send_message(message):
							csock.close()
							break

					elif data == "REBOOT":
						message = "REBOOTING"
						if send_message(message):
							subprocess.Popen(['sudo', 'shutdown','-r','now'])

					elif data == "STOP":
						message = "STOPPING"
						send_message(message)
						shutdown()
						break

					else:
						if data == "GIVE_NAME":
							message = my_name
						elif data == "PLATFORM_INFO":
							message = os.name + " " + platform.system() + " " + platform.release()
						else:
							message = "UNKNOWN_COMMAND"

						sent_bytes = csock.send(message.encode())

						if sent_bytes != 0:
							lights.send_light()
						else:
							lights.fail_light()
				else:
					print("Socket connected, but no data was received.")
					lights.fail_light()
		finally:
			print("CLOSING SOCKET")
			csock.close()
except KeyboardInterrupt:
	shutdown()
