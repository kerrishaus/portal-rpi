from util import display

class ScreenOffCommand():
	def OnExecute(self):
		print("Powering off display")
		display.display_power_off()