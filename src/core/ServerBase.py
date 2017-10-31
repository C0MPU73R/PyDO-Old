import sys
from direct.showbase.ShowBase import ShowBase
from direct.directnotify import DirectNotifyGlobal

from src.util.LogManager import LogManager
from src.dclass.DCManager import DCManager
from src.core.ConnectionManager import ConnectionManager
from src.message.MessageManager import MessageManager
from src.distributed.DistributedObjectManager import DistributedObjectManager
from src.interest.InterestManager import InterestManager


class ServerBase(ShowBase):
    notify = DirectNotifyGlobal.directNotify.newCategory("ServerBase")
    serverVersion = 'pcsv1.0.34.31'

    def __init__(self):
        ShowBase.__init__(self)

        self.activeConnections = {}

        self.configManager = None

        self.logManager = LogManager()
        self.dcManager = DCManager()
        self.connectionManager = ConnectionManager()
        self.messageManager = MessageManager()
        self.doManager = DistributedObjectManager()
        self.interestManager = InterestManager()