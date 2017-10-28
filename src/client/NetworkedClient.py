from direct.directnotify import DirectNotifyGlobal

class NetworkedClient:
	notify = DirectNotifyGlobal.directNotify.newCategory("NetworkedClient")

	def __init__(self):
		self.authed = False

	def handleDatagram(self):
		pass

	def updateHeartbeat(self):
		# TODO: Handle Heartbeat's
		pass

	def setAuthed(self, authed):
		self.authed = authed