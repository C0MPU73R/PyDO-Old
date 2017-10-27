import sys
from panda3d.core import (QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter,
                          PointerToConnection, NetAddress, NetDatagram)
from direct.showbase.ShowBase import ShowBase
from direct.directnotify import DirectNotifyGlobal
from direct.task.Task import Task
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from ServerProtocols import *

from src.util.LogManager import LogManager


class ServerBase(ShowBase):
    notify = DirectNotifyGlobal.directNotify.newCategory("ServerBase")

    def __init__(self):
        ShowBase.__init__(self)

        self.configManager = None
        self.socket = None
        self.connection = None
        self.activeConnections = []
        self.hostName = None
        self.port = None
        self.hostPort = None
        self.ourChannel = 100001

        self.logManager = LogManager()

        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

    def start(self):
        self.hostName = self.configManager.getString('host-name', '127.0.0.1')
        self.port = self.configManager.getInt('port-number', 6667)
        self.hostPort = self.configManager.getInt('host-port-number', 7101)

        self.socket = self.cManager.openTCPServerRendezvous(self.hostName, self.port, 1000)
        if self.socket:
            self.cListener.addConnection(self.socket)
            self._serverStarted(self.hostName, self.port)
            taskMgr.add(self._socketListener, 'Connection Listener')
            taskMgr.add(self._socketReader, 'Connection Reader')
        else:
            self.notify.warning("Unable to start server on %s:%d - is the port in use?" % (self.hostName, self.port))
            self.logManager.writeServerEvent('ServerBase', 'Unable to start server on %s:%d - is the port in use?'
                                             % (self.hostName, self.port))
            sys.exit()

        timeout = 5000
        self.connection = self.cManager.openTCPClientConnection(self.hostName, self.hostPort, timeout)
        if self.connection:
            self.cReader.addConnection(self.connection)
            self.registerChannel(self.ourChannel)
            taskMgr.add(self._socketListener, 'Poll the datagram reader')

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
                self.activeConnections.append(newConnection)
                self.cReader.addConnection(newConnection)
                self.notify.debug("New Client Connected: %s" % (netAddress))

        return Task.cont

    def _socketReader(self, task):
        if self.cReader.dataAvailable():
            datagram = NetDatagram()

            if self.cReader.getData(datagram):
                self.handleDatagram(datagram)

        return Task.cont

    def registerChannel(self, channel):
        dg = PyDatagram()
        dg.addUint16(CONTROL_SET_CHANNEL)
        dg.addUint64(channel)
        self.cWriter.send(dg, self.connection)

    def unregisterChannel(self, channel):
        dg = PyDatagram()
        dg.addUint16(CONTROL_REMOVE_CHANNEL)
        dg.addUint64(channel)
        self.cWriter.send(dg, self.connection)

    def handleDatagram(self, datagram):
        connection = datagram.getConnection()
        dgi = PyDatagramIterator(datagram)
        message_type = dgi.getUint16()

        self.notify.warning("Received data: %s" % str(datagram))
