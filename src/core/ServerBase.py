import sys
from panda3d.core import (QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, 
							PointerToConnection, NetAddress, NetDatagram)
from direct.showbase.ShowBase import ShowBase
from direct.directnotify import DirectNotifyGlobal
from direct.task.Task import Task

from src.util.LogManager import LogManager

class ServerBase(ShowBase):
	notify = DirectNotifyGlobal.directNotify.newCategory("ServerBase")

	def __init__(self):
		ShowBase.__init__(self)

		self.configManager = None
		self.socket = None
		self.hostName = None
		self.port = None

		self.logManager = LogManager()

		self.cManager = QueuedConnectionManager()
		self.cListener = QueuedConnectionListener(self.cManager, 0)
		self.cReader = QueuedConnectionReader(self.cManager, 0)
		self.cWriter = ConnectionWriter(self.cManager, 0)

	def start(self):
		self.hostName = self.configManager.getString('host-name', '127.0.0.1')
		self.port = self.configManager.getInt('port-number', 7101)

		self.socket = self.cManager.openTCPServerRendezvous(self.hostName, self.port, 1000)
		if self.socket:
			self.cListener.addConnection(self.socket)
			self._serverStarted(self.hostName, self.port)
			taskMgr.add(self._socketListener, 'Connection Listener')
			taskMgr.add(self._socketReader, 'Connection Reader')
		else:
			self.notify.warning("Unable to start server on %s:%d - is the port in use?" % (self.hostName, self.port))
			self.logManager.writeServerEvent('ServerBase', 'Unable to start server on %s:%d - is the port in use?' % (host, port))
			sys.exit()

	def _serverStarted(self, host, port):
		self.notify.warning("Server started on %s:%d" % (host, port))
		self.logManager.writeServerEvent('ServerBase', 'Server started on %s:%d' % (host, port))

	def _socketListener(self, task):
		if self.cListener.newConnectionAvailable():
			rendezvous = PointerToConnection()
			netAddress = NetAddress()
			newConnection = PointerToConnection()

			if self.cListener.getNewConnection(rendezvous, netAddress, newConnection):
				newConnection = newConnection.p()
				#self.activeConnections.append(newConnection)
				self.cReader.addConnection(newConnection)
				self.notify.debug("New Client Connected: %s" % (netAddress))

		return Task.cont
	
	def _socketReader(self, task):
		if self.cReader.dataAvailable():
			datagram = NetDatagram()

			if self.cReader.getData(datagram):
				self.handleDatagram(datagram)

		return Task.cont

	def handleDatagram(self, data):
		self.notify.warning("Received Data: %s" % str(data))