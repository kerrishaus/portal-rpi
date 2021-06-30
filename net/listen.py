import socket
import selectors

from util.gpio import lights

s = socket.socket()

def setup():
	s.bind(("0.0.0.0", 27000))

	if s.listen():
		lights.send_light()
	else:
		lights.fail_light()

	s.settimeout(.1)