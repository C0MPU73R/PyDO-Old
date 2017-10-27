from direct.directnotify import DirectNotifyGlobal

class LegacyMessageManager:
	notify = DirectNotifyGlobal.directNotify.newCategory("MessageManager")

	def __init__(self):
		pass

	def handleMessage(self, datagram):
		self.notify.warning("New Message: " + str(datagram))