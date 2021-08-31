from commands import Command

import os

class RebootCommand(Command):
	def OnExecute():
		print("Shutting down...")
		os.system("poweroff")
