import portal
import util.logging
from util.logging import Logger

client = portal.Portal()

if client.Init():
	try:
		while client.running:
			try:
				client.Update()
			except Exception as e:
				Logger.error("Exception occured while running client.Update")
	except KeyboardInterrupt:
		client.Cleanup()
		exit()
else:
	Logger.error("Failed to initialise Portal client.")
	client.Cleanup()
	exit()