import os

class RebootCommand():
	def OnExecute(self):
		print("Shutting down...")
		os.system("poweroff")