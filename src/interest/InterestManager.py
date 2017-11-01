from direct.directnotify import DirectNotifyGlobal
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from src.legacy.LegacyMessageTypes import *


class InterestManager:
	notify = DirectNotifyGlobal.directNotify.newCategory("InterestManager")

	def __init__(self):
		pass

	def registerInterest(self, dgi, connection):
		# The structure of an interest is:
		#	* An Id of the interest
		#	* A context Id
		#	* A parent DoId
		#	* Lastly, a list of zones to listen into

		interestId = dgi.getUint16()
		contextId = dgi.getUint32()
		parentDoId = dgi.getUint32()

		zones = []
		zones.append(dgi.getUint32())

		self.notify.warning("%s - %s - %s - %s" % (interestId, contextId, parentDoId, zones))

		objects = base.doManager.getDoList(parentDoId, zones[0])
		self.notify.warning(objects)

		if zones == [3]: #Found shard list interest
			##Create our PirateDistrict instance
			datagram = PyDatagram()
			datagram.addUint16(CLIENT_CREATE_OBJECT_REQUIRED_RESP)
			datagram.addUint32(4617) #parentId (OTP_DO_ID_PIRATES)
			datagram.addUint32(3)  #zoneId (SHARD LIST INTEREST)
			datagram.addUint16(54) #DCLASS Id

			datagram.addUint32(474000001) #Shard ID (DOID)
			datagram.addString('Yarr!') #setName (distributedDistrict)
			datagram.addUint8(1) #setAvailable (distributedDistrict)
			datagram.addString('') #setParentingRules (1)
			datagram.addString('') #setParentingRules (2)
			datagram.addUint32(0) #setAvatarCount
			datagram.addUint32(0) #setNewAvatarCount          
			datagram.addString('PortRoyalWorld') #setMainWorld
			datagram.addUint8(1) #setShardType

			base.connectionManager.cWriter.send(datagram, connection) #FLOOR IT

			##Create our PirateTimeManager instance
			datagram = PyDatagram()
			datagram.addUint16(CLIENT_CREATE_OBJECT_REQUIRED_RESP)
			datagram.addUint32(4617) #parentId (OTP_DO_ID_PIRATES)
			datagram.addUint32(3)  #zoneId (SHARD LIST INTEREST)
			datagram.addUint16(172) #DCLASS Id

			datagram.addUint32(474000002) #Shard ID (DOID)

			base.connectionManager.cWriter.send(datagram, connection) #FLOOR IT

		datagram = PyDatagram()
		#datagram.addServerHeader(interestId, 474000001, CLIENT_DONE_INTEREST_RESP)
		datagram.addUint16(CLIENT_DONE_INTEREST_RESP)
		datagram.addUint16(interestId)
		datagram.addUint32(contextId)
		datagram.addUint32(parentDoId)
		datagram.addUint32(zones[0])

		base.connectionManager.cWriter.send(datagram, connection)