from panda3d.core import loadPrcFile, ConfigVariableBool, ConfigVariableString, ConfigVariableInt

class ConfigManager:

	def __init__(self):
		loadPrcFile('config/general.prc')
		
	def getBool(self, var, default):
		return ConfigVariableBool(var, default).getValue()

	def getString(self, var, default):
		return ConfigVariableString(var, default).getValue()

	def getInt(self, var, default):
		return ConfigVariableInt(var, default).getValue()