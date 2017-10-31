from direct.directnotify import DirectNotifyGlobal
from DoHierarchy import DoHierarchy


class DistributedObjectManager:
	notify = DirectNotifyGlobal.directNotify.newCategory("DistributedObjectManager")

	def __init__(self):
		self.dclassesByName = base.dcManager.dclassesByName

		# Dict of {DistributedObject ids: DistributedObjects}
		self.doId2do = {}
		# (parentId, zoneId) to dict of doId->DistributedObjectAI

		# TODO: Owner View
		self.doId2ownerView = {}

		# The Distributed Object Hierarchy
		self._doHierarchy = DoHierarchy()

	def storeObjectLocation(self, object, parentId, zoneId):
		oldParentId = object.parentId
		oldZoneId = object.zoneId

		if (oldParentId != parentId):
			# notify any existing parent that we're moving away
			oldParentObj = self.doId2do.get(oldParentId)
			if oldParentObj is not None:
				oldParentObj.handleChildLeave(object, oldZoneId)

			self.deleteObjectLocation(object, oldParentId, oldZoneId)

		elif (oldZoneId != zoneId):
			# Remove old location
			oldParentObj = self.doId2do.get(oldParentId)
			if oldParentObj is not None:
				oldParentObj.handleChildLeaveZone(object, oldZoneId)

			self.deleteObjectLocation(object, oldParentId, oldZoneId)

		else:
			# object is already at that parent and zone
			return

		if ((parentId is None) or (zoneId is None) or (parentId == zoneId == 0)):
			# Do not store null values
			object.parentId = None
			object.zoneId = None

		else:
			# Add to new location
			self._doHierarchy.storeObjectLocation(object, parentId, zoneId)
			# this check doesn't work because of global UD objects;
			# should they have a location?
			#assert len(self._doHierarchy) == len(self.doId2do)

			# Set the new parent and zone on the object
			object.parentId = parentId
			object.zoneId = zoneId

		if oldParentId != parentId:
			# Give the parent a chance to run code when a new child
			# sets location to it. For example, the parent may want to
			# scene graph reparent the child to some subnode it owns.
			parentObj = self.doId2do.get(parentId)
			if parentObj is not None:
				parentObj.handleChildArrive(object, zoneId)

			elif parentId not in (None, 0, self.getGameDoId()):
				self.notify.warning('storeObjectLocation(%s): parent %s not present' % (object.doId, parentId))

		elif oldZoneId != zoneId:
			parentObj = self.doId2do.get(parentId)
			if parentObj is not None:
				parentObj.handleChildArriveZone(object, zoneId)

			elif parentId not in (None, 0, self.getGameDoId()):
				self.notify.warning('storeObjectLocation(%s): parent %s not present' % (object.doId, parentId))

	def isValidLocationTuple(self, location):
		return (location is not None and location != (0xffffffff, 0xffffffff) and location != (0, 0))

	def getDoTable(self, ownerView):
		# TODO
		if ownerView:
			assert self.hasOwnerView()
			return self.doId2ownerView
		else:
			return self.doId2do

	# TODO: Owner Views, how do we handle them serverside?
	def addDOToTables(self, do, location=None, ownerView=False):
		if not ownerView:
			if location is None:
				location = (do.parentId, do.zoneId)

		doTable = self.getDoTable(ownerView)

		if do.doId in doTable:
			if ownerView:
				tableName = 'doId2ownerView'
			else:
				tableName = 'doId2do'

			self.notify.warning("doId '%s' already exists in doTable!" % do.doId)

		doTable[do.doId] = do

		if not ownerView:
			if self.isValidLocationTuple(location):
				self.storeObjectLocation(do, location[0], location[1])