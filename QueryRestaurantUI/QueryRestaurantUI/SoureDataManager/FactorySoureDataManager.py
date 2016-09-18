from mySQLSoureDataManager import mySQLSoureDataManager
from mySQLSUSDataManager import mySQLSUSDataManager

def GetSourceDataManager(configXML, logWriter = None):
    config = type('config', (object,), {}) 
    config.databaseName = configXML.queryserver.souredatamanager.databasename.string
    config.user = configXML.queryserver.souredatamanager.user.string
    config.password = configXML.queryserver.souredatamanager.password.string
    config.host = configXML.queryserver.souredatamanager.host.string
    return mySQLSoureDataManager(config, logWriter)

def GetSUSDataManager(configXML, logWriter = None):
    config = type('config', (object,), {})
    config.databaseName = configXML.queryserver.susdatamanager.databasename.string
    config.user = configXML.queryserver.susdatamanager.user.string
    config.password = configXML.queryserver.susdatamanager.password.string
    config.host = configXML.queryserver.susdatamanager.host.string
    return mySQLSUSDataManager(config, logWriter)
