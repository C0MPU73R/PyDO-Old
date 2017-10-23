import os, sys
from datetime import datetime
from panda3d.core import MultiplexStream, Filename, Notify, pofstream, StreamWriter

class LogOutput:

	def __init__(self, parent, origin, logFile):
		self.parent = parent
		self.origin = origin
		self.logFile = logFile
		self.console = False

	def write(self, message):
		self.parent.writeServerEvent('Python', message)
		if self.console:
			self.parent.writeServerEvent('Python', message)

class LogManager:

	def __init__(self):
		if not os.path.exists('logs/'):
			os.makedirs('logs')

		self.logSuffix = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
		self.logName = 'logs/pydo-' + self.logSuffix + '.log'

		self.logFile = open(self.logName, 'a+')

		self.logOutput = LogOutput(self, sys.__stdout__, self.logFile)
		self.logError = LogOutput(self, sys.__stderr__, self.logFile)

		sys.stdout = self.logOutput
		sys.stderr = self.logError

	def writeServerEvent(self, origin, message):
		timeStamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.logFile.write(timeStamp + ' - ' + origin + ' : ' + message + '\n')
		self.logFile.flush()