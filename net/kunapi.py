import requests

from .util import lights

def post(endpoint, payload):
	r = requests.post("https://api.kunindustries.com/portal/devices/" + endpoint + ".php", data = payload)
	lights.send_light()
	return r

#def get(endpoint, payload):
#	r = requests.get("https://api.kunindustries.com/portal/devices/" + endpoint + ".php", data = payload)
#	lights.send_light()
#	return r