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
		elif messageType == CLIENT_DISCONNECT:
			self.handleClientDisconnected(dgi, connection)
		elif messageType == CLIENT_LOGIN_3:
			self.handleClientLogin(dgi, connection)
		elif messageType == CLIENT_ADD_INTEREST:
			self.handleAddInterest(dgi, connection)
		else:
			self._unimplementedType(messageType)

	def handleClientHeartbeat(self, dgi, connection):
		base.activeConnections[connection].updateHeartbeat()

	def handleClientDisconnected(self, dgi, connection):
		base.connectionManager.cManager.closeConnection(connection)
		del base.activeConnections[connection]

	def handleClientLogin(self, dgi, connection):
		# Let's get the client's loginToken and supplied serverVersion
		loginToken = dgi.getString()
		serverVersion = dgi.getString()

		if serverVersion != base.serverVersion:
			# Boot them out
			self.notify.warning("Client version (%s) mismatch with server version (%s)! Booting them out..." % (serverVersion, base.serverVersion))

			datagram = PyDatagram()
			datagram.addUint16(CLIENT_GO_GET_LOST)
			datagram.addUint16(125)
			  
			base.connectionManager.cWriter.send(datagram, connection)
			return

		base.activeConnections[connection].setAuthed(True)

		if base.loginInterface:
			base.loginInterface.login(dgi, connection)
		else:
			self.notify.warning("Received login message without a set loginInterface")
			base.logManager.writeServerEvent('MessageManager', "Received login message without a set loginInterface")

	def handleAddInterest(self, dgi, connection):
		pass

	def _unimplementedType(self, type):
		self.notify.warning("Unknown Message Type: " + str(type))
		base.logManager.writeServerEvent('MessageManager', 'Unknown Message Type: %s' % str(type))