import os

class ShutdownCommand():
	def OnExecute(self):
		print("Shutting down...")
		os.system("poweroff") # the pi cannot actually be shut down