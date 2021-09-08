import os

class RebootCommand():
	def OnExecute(self):
		print("Rebooting...")
		os.system("poweroff") # it will just boot again, because it's an rpi
		
		#subprocess.Popen(['sudo', 'shutdown','-r','now'])