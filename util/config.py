import configparser
import os

configLocation = "/home/pi/portal-rpi/config.ini"
config = configparser.ConfigParser()

def write_file():
	config.write(open(configLocation, 'w'))

if not os.path.exists(configLocation):
	config['DEFAULT']['MyName'] = "Raspberry Pi"
	config['DEFAULT']['MyAddr'] = "0.0.0.0"
	config['DEFAULT']['MyPort'] = "27000"
	config['DEFAULT']['MyPurpose'] = "Develop"

	config['KUNINDUSTRIES_API']['Token'] = "NO-TOKEN"
	config['KUNINDUSTRIES_API']['StatusInterval'] = 60
	config['KUNINDUSTRIES_API']['AutoUpdateAddressAndPort'] = True
	config['KUNINDUSTRIES_API']['DeviceID'] = 0

	write_file()
else:
	config.read(configLocation)

	my_name = config['DEFAULT']['MyName']
	my_addr = config['DEFAULT']['MyAddr']
	my_port = int(config['DEFAULT']['MyPort'])
	my_purpose = config['DEFAULT']['MyPurpose']

	api_token = config['KUNINDUSTRIES_API']['Token']
	api_status_interval = float(config['KUNINDUSTRIES_API']['StatusInterval'])
	api_auto_update_addr_and_port = config['KUNINDUSTRIES_API']['AutoUpdateAddressAndPort']
	api_device_id = config['KUNINDUSTRIES_API']['DeviceID']

def updateConfig(section, key, value):
	config[section][key] = value

	write_file()