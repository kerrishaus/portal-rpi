import requests

from util import config
from util.gpio import lights

def post(endpoint, payload):
	r = requests.post("https://api.kerrishaus.com/portal/devices/" + endpoint + ".php", data = payload)
	if r.status_code:
		lights.send_light()
	else:
		lights.fail_light()
	return r

#def get(endpoint, payload):
#	r = requests.get("https://api.kerrishaus.com/portal/devices/" + endpoint + ".php", data = payload)
#	lights.send_light()
#	return r

STATUS_OFFLINE   = 0
STATUS_ONLINE    = 1
STATUS_MOTION    = 3
STATUS_NO_MOTION = 4

def status(status):
	payload = {
		"deviceid": config.api_device_id,
		"status": status,
		"token": "NO-TOKEN"
	}

	return post("status", payload)