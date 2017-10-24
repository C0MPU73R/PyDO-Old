from TestOutput import LogManager

class Auth_Test:

	def __init__(self):
		self.logger = LogManager('AuthTest')
		self.logger.writeTestEvent('AuthTest', 'Test Started')

if __name__ == "__main__":
	Auth_Test()