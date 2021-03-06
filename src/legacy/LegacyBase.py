from src.core.ServerBase import ServerBase

from src.legacy.LegacyMessageManager import LegacyMessageManager

'''
LegacyBase is for use by projects that are emulating Disney's OTP server
and inherently its structure. This class inherits from ServerBase (The standard
base for PyDO) and adds in its own custom handlers.
'''


class LegacyBase(ServerBase):

	def __init__(self):
		ServerBase.__init__(self)

		self.loginInterface = None

		self.messageManager = LegacyMessageManager()