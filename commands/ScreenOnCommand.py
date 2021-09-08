from util import display

class ScreenOnCommand():
	def OnExecute(self):
		print("Powering on display")
		display.display_power_on()