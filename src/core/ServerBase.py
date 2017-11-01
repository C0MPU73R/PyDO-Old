import sys
from direct.showbase.ShowBase import ShowBase
from direct.directnotify import DirectNotifyGlobal
from panda3d.core import UniqueIdAllocator

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

        maxChannels = self.config.GetInt('max-channel-id', 1000000)
        self.channelAllocator = UniqueIdAllocator(0, 0+maxChannels-1)

        self.configManager = None

        self.logManager = LogManager()
        self.dcManager = DCManager()
        self.dcManager.readDCFile()
        self.notify.warning(str(self.dcManager.dclassesByName))
        self.connectionManager = ConnectionManager()
        self.messageManager = MessageManager()
        self.doManager = DistributedObjectManager()
        self.interestManager = InterestManager()