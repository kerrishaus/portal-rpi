import configparser
import os

configLocation = "/home/pi/portal-rpi/config.ini"
config = configparser.ConfigParser()

def write_file():
	config.write(open(configLocation, 'w'))

if not os.path.exists(configLocation):
	config['DEFAULT'] = { 'MyName': "Raspberry Pi", 'MyAddr': "0.0.0.0", 'MyPort': "27000", 'MyPurpose': "Develop" }
	config['SCREEN'] = { 'IdleTime': "15" }
	config['KUNINDUSTRIES_API'] = { 'Token': "NO-TOKEN", 'StatusInterval': 60, 'AutoUpdateAddressAndPort': True, 'DeviceID': 0 }

	write_file()
else:
	config.read(configLocation)

my_name = config['DEFAULT']['MyName']
my_addr = config['DEFAULT']['MyAddr']
my_port = int(config['DEFAULT']['MyPort'])
my_purpose = config['DEFAULT']['MyPurpose']

# this value is in seconds
screen_idle_time = int(config['SCREEN']['IdleTime'])

api_token = config['KUNINDUSTRIES_API']['Token']
api_status_interval = float(config['KUNINDUSTRIES_API']['StatusInterval'])
api_auto_update_addr_and_port = config['KUNINDUSTRIES_API']['AutoUpdateAddressAndPort']
api_device_id = config['KUNINDUSTRIES_API']['DeviceID']

def updateConfig(section, key, value):
	config[section][key] = value

	write_file()