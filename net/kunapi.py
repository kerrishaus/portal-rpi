import requests

import lights

def post_api(endpoint, payload):
	r = requests.post("https://api.kunindustries.com/portal/devices/" + endpoint + ".php", data = payload)
	lights.send_light()
	return r