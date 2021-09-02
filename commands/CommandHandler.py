class CommandHandler:
	commands = {}

	def RegisterCommand(self, commandClass, commandName):
		self.commands[commandName] = (commandClass)
		print("Registered command " + commandName)

	def runCommand(self, commandName):
		if commandName in self.commands:
			self.commands[commandName].OnExecute()