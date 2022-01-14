import socket
import selectors

from util import config
from util.gpio import lights

s = socket.socket()

def setup():
	s.bind(("0.0.0.0", config.my_port))

	if s.listen():
		lights.send_light()
	else:
		lights.fail_light()

	s.settimeout(.1)
	
	print("Listener started on port " + string(config.my_port))
