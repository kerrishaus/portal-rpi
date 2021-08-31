class CommandHandler:
	commands = {}

	def RegisterCommand(commandClass, commandName):
		self.commands[commandName] = (commandClass)
		print("Registered command " + commandName)

	def runCommand(commandName):
		self.commands[commandName].OnExecute()