from commands import Command

import os

class RebootCommand(commands.Command):
	def OnExecute():
		print("Shutting down...")
		os.system("poweroff")
