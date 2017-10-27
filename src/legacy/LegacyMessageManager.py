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
		# TODO: This is being hard set for pirates. We need to abstract this out so people can write their own login logic.

		# Let's get their loginToken and supplied serverVersion
		loginToken = dgi.getString()
		serverVersion = dgi.getString()

		datagram = PyDatagram()

		datagram.addUint16(CLIENT_LOGIN_3_RESP) #msgType

		datagram.addUint8(0) #returnCode
		datagram.addString("") #errorString

		## account details 
		datagram.addString("YES") #OpenChatEnabled
		datagram.addString("YES") #CreateFriendsWithChat
		datagram.addString("YES") #ChatCodeCreation
		datagram.addString("FULL") #PiratesAccess
		datagram.addInt32(0) #FamilyAccountId
		datagram.addInt32(346056549) #PlayerAccountId
		datagram.addString("developer") #PlayerName
		datagram.addInt8(1) #AccountNameApproved
		datagram.addInt32(2) #MaxAvatars
		datagram.addUint16(1) #NumSubs

		## account's sub
		datagram.addUint32(346056549) #subId
		datagram.addUint32(346056549) #subOwnerId
		datagram.addString("developer") #subName
		datagram.addString("YES") #subActive
		datagram.addString("FULL") #subAccess
		datagram.addUint8(1) #subLevel
		datagram.addUint8(2) #subNumAvatars
		datagram.addUint8(1) #subNumConcur
		datagram.addString("YES") #subFounder 

		base.connectionManager.cWriter.send(datagram, connection)

	def _unimplementedType(self, type):
		self.notify.warning("Unknown Message Type: " + str(type))
		base.logManager.writeServerEvent('MessageManager', 'Unknown Message Type: %s' % str(type))