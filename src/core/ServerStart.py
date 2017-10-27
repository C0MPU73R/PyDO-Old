import sys
import __builtin__

try:
    from panda3d.core import *
except:
    print(":ServerStart(error): Panda3D is required to run PyDO")
    sys.exit()

from src.config.ConfigManager import ConfigManager

configManager = ConfigManager()

isLegacy = configManager.getBool('want-legacy', False)
if isLegacy:
    from src.legacy.LegacyBase import LegacyBase
    __builtin__.base = LegacyBase()
else:
    from src.core.ServerBase import ServerBase
    __builtin__.base = ServerBase()

base.configManager = configManager

base.connectionManager.start()
base.run()