import os, sys
from datetime import datetime

class LogOutput:

	def __init__(self, parent, origin, logFile):
		self.parent = parent
		self.origin = origin
		self.logFile = logFile
		self.console = False

	def write(self, message):
		self.parent.writeTestEvent('Python', message + '\n')
		if self.console:
			self.parent.writeTestEvent('Python', message + '\n')

class LogManager:

	def __init__(self, testName):
		if not os.path.exists('test_logs/'):
			os.makedirs('test_logs')

		self.testName = testName
		self.logSuffix = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
		self.logName = 'test_logs/' + self.testName + '-' + self.logSuffix + '.log'

		self.logFile = open(self.logName, 'a+')

		self.logOutput = LogOutput(self, sys.__stdout__, self.logFile)
		self.logError = LogOutput(self, sys.__stderr__, self.logFile)

		sys.stdout = self.logOutput
		sys.stderr = self.logError

	def writeTestEvent(self, origin, message):
		timeStamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.logFile.write(timeStamp + ' - ' + origin + ' : ' + message)
		self.logFile.flush()