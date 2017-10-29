from direct.directnotify import DirectNotifyGlobal


class DistributedObjectManager:
	notify = DirectNotifyGlobal.directNotify.newCategory("DistributedObjectManager")

	def __init__(self):
		self.globalObjects = {}

	def generateOTPObject(self, parentId, zoneId, object):
		# TODO: Figure out how we are going to create our tree structure for parent's and their children/zones.
		# (Similar to NodePath)
		pass