import requests

from util import config
from util.gpio import lights

ip = get('https://api.ipify.org').content.decode('utf8')
print("This device's public ip is: {}".format(ip))

def post(endpoint, payload):
	try:
		r = requests.post("https://api.kerrishaus.com/portal/devices/" + endpoint + ".php", data = payload)
		if r.status_code:
			lights.send_light()
		else:
			lights.fail_light()
		return r
	except Exception as e:
		print("Exception raised in KerrisHausAPI... typical.")

#def get(endpoint, payload):
#	r = requests.get("https://api.kerrishaus.com/portal/devices/" + endpoint + ".php", data = payload)
#	lights.send_light()
#	return r

STATUS_OFFLINE   		    = 0
STATUS_ONLINE    		    = 1
STATUS_ONLINE_SCREEN_ON     = 2
STATUS_ONLINE_SCREEN_OFF    = 3
STATUS_MOTION_DETECTED      = 4
STATUS_STOP_MOTION_DETECTED = 5

UPDATE_SCREEN_OFF = 6
UPDATE_SCREEN_ON  = 7

def status(status):
	payload = {
		"deviceid": config.api_device_id,
		"status": status,
		"token": config.api_token,
		"ip": ip
	}

	return post("status", payload)

def notify_screen(screen_state):
	payload = {
		"deviceid": config.api_device_id,
		"status": screen_state,
		"token": config.api_token
	}

	return post("update", payload)
