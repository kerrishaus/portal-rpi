from util.logging import Logger
from util import config
from util import gpio
from util.gpio import lights
from util.gpio import motion
from util import timer
from util import display

from commands import CommandHandler
from commands import ShutdownCommand
from commands import RebootCommand
from commands import PingCommand

from net import listen
from net import kerrishausapi

import os
import platform
import json
import socket

PORTAL_VERSION = 1

class Portal():
	def Init(self):
		Logger.info("Initialising Portal")

		# config is currently autoloaded
		#config.load_config()

		print("Starting Portal client " + str(PORTAL_VERSION))
		print("My name is " + config.my_name + ".")
		print("I am device " + config.api_device_id)
		print("My purpose is " + config.my_purpose)

		gpio.setup()
		lights.setup()
		listen.setup()

		if "Motion" in config.my_purpose:
			motion.setup()

		self.cman = CommandHandler.CommandHandler()

		self.cman = CommandHandler.CommandHandler()
		self.cman.RegisterCommand(ShutdownCommand.ShutdownCommand(), "SHUTDOWN")
		self.cman.RegisterCommand(RebootCommand.RebootCommand(), "REBOOT")
		self.cman.RegisterCommand(PingCommand.PingCommand(), "TELL_HIM_HES_UGLY")

		if "Kiosk" in config.my_purpose:
			from commands import ScreenOffCommand
			from commands import ScreenOnCommand

			self.cman.RegisterCommand(ScreenOffCommand.ScreenOffCommand(), "SCREEN_OFF")
			self.cman.RegisterCommand(ScreenOnCommand.ScreenOnCommand(), "SCREEN_ON")

		self.api_timer = timer.Timer()
		self.light_timer = timer.Timer()

		self.running = True

		Logger.info("I'm ready! I'm ready! I'm ready!")
		return

	def Cleanup(self):
		print("Portal service is stopping...")
		self.running = False
				
		gpio.cleanup()
		listen.s.close()

		kerrishausapi.status(0)
		Logger.info("Have a good night.")

	def Update(self):
		if self.api_timer.getElapsedTime() > config.api_status_interval:
			if "Kiosk" in config.my_purpose:
				if display.is_display_powered():
					kerrishausapi.status(2)
				else:
					kerrishausapi.status(3)
			else:
				kerrishausapi.status(1)

			self.api_timer.reset()

		if "Motion" in config.my_purpose:
			motion.update()

		try:
			csock, caddr = listen.s.accept()
			csock.settimeout(.1)
			invalidDataCount = 0
			print("/ ACCEPTED SOCKET")
			try: # this is the client communication loop
				while True:
					data = csock.recv(1024)
					if data:
						lights.recv_light()

						data = data.decode()
						print("> " + data)

						self.cman.runCommand(data)

						if data == "DISCONNECT":
							if listen.send_message("BYE_BYE", csock):
								csock.close()
								break

						elif data == "SET_NAME":
							listen.send_message("OKAY_GIVE_NAME", csock)

							data = csock.recv(1024)
							if data:
								new_name = data.decode()
								config.updateConfig("DEFAULT", "MyName", new_name)
								config.my_name = new_name
								print("my new name is " + config.my_name)
								listen.send_message("NAME_SET", csock)
							else:
								print("NO name given")
								listen.send_message("FAIL_INVALID_DATA", csock)

						elif data == "SET_API_INTERVAL":
							listen.send_message("OKAY_GIVE_INTERVAL", csock)

							data = csock.recv(1024)
							if data:
								new_interval = data.decode()
								config.updateConfig("KUNINDUSTRIES_API", "StatusInterval", new_interval)
								config.api_status_interval = new_interval
								print("Status interval set to " + config.api_status_interval)
								listen.send_message("INTERVAL_SET", csock)
							else:
								print("Data is invalid.")
								listen.send_message("FAIL_INVALID_DATA", csock)

						elif data == "GIVE_PURPOSE":
							listen.send_message(config.my_purpose, csock)

						elif data == "SCREEN_STATUS":
							listen.send_message(display.is_display_powered(), csock)

						elif data == "PLATFORM_INFO":
							listen.send_message(os.name + " " + platform.system() + " " + platform.release() + " " + platform.machine(), csock)

						elif data == "GIVE_NAME":
							listen.send_message(config.my_name, csock)

						elif data == "GIVE_GENERAL":
							if "Kiosk" in config.my_purpose:
								screen = {
									"powered": display.is_display_powered()
								}
							else:
								screen = False

							if "Motion" in config.my_purpose:
								motion_stat = motion.motion
							else:
								motion_stat = False

							payload = {
								"deviceid": config.api_device_id,
								"name": config.my_name,
								"platform": os.name + " " + platform.system() + " " + platform.release() + " " + platform.machine(),
								"purpose": config.my_purpose,
								"screen": screen,
								"motion": motion_stat,
							}

							payload = json.dumps(payload)

							listen.send_message(payload, csock)

						else:
							listen.send_message("UNKNOWN_COMMAND", csock)
					else:
						Logger.error("Data received, but data was invalid.")
						lights.fail_light()

						data = None; del data
						invalidDataCount += 1

						if invalidDataCount > 20:
							print("| CLOSING SOCKET (too much invalid data)")
							csock.close()
							break
						
			except socket.timeout:
				Logger.warn("Socket timed out.")
			finally:
				print("\ CLOSING SOCKET")
				csock.close()

		except socket.timeout:
			Logger.warn("Socket timed out.")