from direct.directnotify import DirectNotifyGlobal


class MessageManager:
	notify = DirectNotifyGlobal.directNotify.newCategory("MessageManager")

	def __init__(self):
		pass

	def handleMessage(self, datagram):
		pass