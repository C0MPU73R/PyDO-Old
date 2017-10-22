import os, sys
from datetime import datetime

class LogOutput:

	def __init__(self, origin, logFile):
		self.origin = origin
		self.logFile = logFile

	def write(self, str):
		self.logFile.write(str)
		self.logFile.flush()
		self.origin.write(str)
		self.origin.flus()

	def flush(self):
		self.logFile.flush()
		self.origin.flush()

class LogManager:

	def __init__(self):
		if not os.path.exists('logs/'):
			os.makedirs('logs')

		logSuffix = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
		self.logName = 'pydo-' + logSuffix + '.log'

		self.logFile = open('logs/' + self.logName, 'a+')

		self.logOutput = LogOutput(sys.__stdout__, self.logFile)
		self.logError = LogOutput(sys.__stderr__, self.logFile)

		sys.stdout = self.logOutput
		sys.stderr = self.logError