from direct.directnotify import DirectNotifyGlobal
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from src.legacy.LegacyMessageTypes import *


class LegacyMessageManager:
	notify = DirectNotifyGlobal.directNotify.newCategory("MessageManager")

	def __init__(self):
		pass

	def handleMessage(self, datagram):
		# Who sent us the message?
		connection = datagram.getConnection()

		dgi = PyDatagramIterator(datagram)
		messageType = dgi.getUint16()

		if messageType == CLIENT_HEARTBEAT:
			self.handleClientHeartbeat(dgi, connection)
		elif messageType == CLIENT_LOGIN_3:
			self.handleClientLogin(dgi, connection)
		else:
			self._unimplementedType(messageType)

	def handleClientHeartbeat(self, dgi, connection):
		# We got a client heartbeat!
		# TODO: Handle inactive clients
		pass

	def handleClientLogin(self, dgi, connection):
		if base.loginInterface:
			base.loginInterface.login(dgi, connection)
		else:
			self.notify.warning("Received login message without a set loginInterface")
			base.logManager.writeServerEvent('MessageManager', "Received login message without a set loginInterface")

	def _unimplementedType(self, type):
		self.notify.warning("Unknown Message Type: " + str(type))
		base.logManager.writeServerEvent('MessageManager', 'Unknown Message Type: %s' % str(type))