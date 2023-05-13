import socket
import selectors

from util import config
from util.gpio import lights

portalSocket = socket.socket()

def setup():
	portalSocket.bind(("0.0.0.0", config.my_port))

	if portalSocket.listen():
		lights.send_light()
	else:
		lights.fail_light()

	portalSocket.settimeout(.1)
	
	print("Listener started on port " + str(config.my_port))
