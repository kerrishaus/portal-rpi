import time
import os
import platform
import subprocess
import json
import sys
import io
import socket

from util import timer
from util import config
from util import display

from net import Socket
from net import kerrishausapi

from commands import CommandHandler
from commands import ShutdownCommand
from commands import RebootCommand
from commands import PingCommand

if len(sys.argv) > 0:
	if "-install" in sys.argv:
		# TODO: make sure we have privileges to do this
		subprocess.run('''
			echo "Installing systemd services."

			cd /etc/systemd/system/
			touch portal.service

			{
				echo "[Unit]"
				echo "Description=Portal Client Backend"
				echo "Wants=network-online.target"
				echo "After=network-online.target"
				echo ""
				echo "[Service]"
				echo "User=kiosk"
				echo "Type=simple"
				echo "Restart=always"
				echo "ExecStart=/usr/bin/python3 -u /home/kiosk/portal-rpi/portal.py"
				echo ""
				echo "[Install]"
				echo "WantedBy=multi-user.target"
			} > portal.service

			touch portal-gui.service

			{
				echo "[Unit]"
				echo "Description=Portal GUI"
				echo "Requires=portal.service"
				echo "After=network-online.target"
				echo ""
				echo "[Service]"
				echo "User=kiosk"
				echo "Type=simple"
				echo "Restart=always"
				# make sure to modify chrome config and change exited cleanly to true and export the proper display
				echo "Environment=DISPLAY=:0"
				echo "ExecStart=chromium-browser --noerrdialogs --disable-infobars --disable-error-bubbles --ignore-certificate-errors --check-for-update-interval=31536000 --autoplay-policy=no-user-gesture-required --kiosk /home/kiosk/portal_login.html"
				echo ""
				echo "[Install]"
				echo "WantedBy=multi-user.target"
			} > portal-gui.service

			systemctl daemon-reload
			systemctl enable portal.service
			systemctl enable portal-gui.service

			echo "Installed and enabled Portal Client Backend and Portal GUI services."
		''', shell=True)

#from urllib.request import urlopen
#from zipfile import ZipFile

# gonna try downloading sounds and playing them
#zipurl = 'https://kerrishaus.com/packages/portal-rpi-sounds.zip'
    # Download the file from the URL
#zipresp = urlopen(zipurl)
    # Create a new file on the hard drive
#tempzip = open("./resources/sounds.zip", "wb")
    # Write the contents of the downloaded file into the new file
#tempzip.write(zipresp.read())
    # Close the newly-created file
#tempzip.close()
    # Re-open the newly-created file with ZipFile()
#zf = ZipFile("./resources/sounds.zip")
    # Extract its contents into <extraction_path>
    # note that extractall will automatically create the path
#zf.extractall(path = './resources/sounds')
    # close the ZipFile instance
#zf.close()

# TODO: put this in util somewhere
def isRaspberryPi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): 
                return True
            print(m.read())
    except Exception as e:
        print("An exception occured trying to read device model.", e)

    return False

cman = CommandHandler.CommandHandler()
cman.RegisterCommand(ShutdownCommand.ShutdownCommand(), "SHUTDOWN")
cman.RegisterCommand(RebootCommand.RebootCommand(), "REBOOT")
cman.RegisterCommand(PingCommand.PingCommand(), "TELL_HIM_HES_UGLY")

if "Kiosk" in config.my_purpose:
	from commands import ScreenOffCommand
	from commands import ScreenOnCommand

	cman.RegisterCommand(ScreenOffCommand.ScreenOffCommand(), "SCREEN_OFF")
	cman.RegisterCommand(ScreenOnCommand.ScreenOnCommand(), "SCREEN_ON")

VERSION = 1

print("Starting Portal client ", VERSION)

# config is currently autoloaded
#config.load_config()

print("My name is " + config.my_name + ".")
print("I am device " + config.api_device_id)
print("My purpose is " + config.my_purpose)

if isRaspberryPi():
	print("Setting up as Raspberry Pi")
	from util import gpio
	from util.gpio import lights
	gpio.setup()
	lights.setup()

Socket.setup()

kerrishausapi.status(1)

lights.send_light()

print("Portal Client is ready.")

if "Motion-PassiveIR" in config.my_purpose:
	from util.gpio.motion import passiveir
	passiveir.setup()
elif "Motion-Radar" in config.my_purpose:
	from util.gpio.motion import radar
	radar.setup()

def shutdown():
	print("Portal service is stopping...")

	if not kerrishausapi.status(0):
		lights.fail_light()

	lights.fail_light(3)

	gpio.cleanup()
	Socket.portalSocket.close()
 
	print("Have a good night.")

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
			print("API timer reached.")

			if "Kiosk" in config.my_purpose:
				if display.is_display_powered():
					kerrishausapi.status(2)
				else:
					kerrishausapi.status(3)
			else:
				kerrishausapi.status(1)

			api_timer.reset()

		if "Motion-PassiveIR" in config.my_purpose:
			passiveir.update()
		elif "Motion-Radar" in config.my_purpose:
			radar.update()

		try:
			csock, caddr = Socket.portalSocket.accept()
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

						cman.runCommand(data)

						if data == "DISCONNECT":
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
								config.updateConfig("KERRISHAUS_API", "StatusInterval", new_interval)
								config.api_status_interval = new_interval
								print("Status interval set to " + config.api_status_interval)
								send_message("INTERVAL_SET")
							else:
								print("Data is invalid.")
								send_message("FAIL_INVALID_DATA")

						elif data == "GIVE_PURPOSE":
							send_message(config.my_purpose)

						elif data == "SCREEN_STATUS":
							send_message(display.is_display_powered())

						elif data == "PLATFORM_INFO":
							send_message(message = os.name + " " + platform.system() + " " + platform.release() + " " + platform.machine())

						elif data == "GIVE_NAME":
							send_message(config.my_name)

						elif data == "GIVE_GENERAL":
							if "Kiosk" in config.my_purpose:
								screen = {
									"powered": display.is_display_powered()
								}
							else:
								screen = False

							if "Motion-PassiveIR" in config.my_purpose:
								motion_stat = passiveir.motion
							elif "Motion-PassiveIR" in config.my_purpose:
								motion_stat = radar.motion
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

							send_message(payload)

						else:
							send_message("UNKNOWN_COMMAND")
					else:
						print("Data received, but data was invalid.")
						lights.fail_light()

						data = None; del data
						invalidDataCount += 1

						if invalidDataCount > 20:
							print("| CLOSING SOCKET (too much invalid data)")
							csock.close()
							break
						
			except socket.timeout:
				print("socket timeout")
			finally:
				print("\ CLOSING SOCKET")
				csock.close()
		except socket.timeout:
			continue
except KeyboardInterrupt:
	print("STOP")
	shutdown()
	exit()

shutdown()
