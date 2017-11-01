from direct.directnotify import DirectNotifyGlobal
from DoCollectionManager import DoCollectionManager


class DistributedObjectManager(DoCollectionManager):
	notify = DirectNotifyGlobal.directNotify.newCategory("DistributedObjectManager")

	def __init__(self):
		DoCollectionManager.__init__(self)

		self.dclassesByName = base.dcManager.dclassesByName

		self.serverId = 0
		self.ourChannel = 0

	def allocateChannel(self):
		return base.channelAllocator.allocate()

	def send(self, datagram):
		# Zero-length datagrams might freak out the server.  No point
		# in sending them, anyway.
		if datagram.getLength() > 0:
			pass
			#base.connectionManager.cWriter.sendDatagram(datagram)

	def getGameDoId(self):
		return 4617

	def hasOwnerView(self):
		return False