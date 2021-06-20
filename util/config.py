import configparser

config = configparser.ConfigParser()
config.read('config.ini')

my_name = config['DEFAULT']['MyName']
api_token = config['KUNINDUSTRIES_API']['Token']
api_status_interval = config['KUNINDUSTRIES_API']['StatusInterval']
api_status_interval = config['KUNINDUSTRIES_API']['AutoUpdateAddressAndPort']
api_device_id = config['KUNINDUSTRIES_API']['DeviceID']

def updateConfig(section, key, value):
	config[section][key] = value

	with open('db3.ini', 'w') as configfile:
	    config.write(configfile)