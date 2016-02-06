from mySQLSoureDataManager import mySQLSoureDataManager


def GetSourceDataManager(configXML, logWriter = None):
    config = type('config', (object,), {}) 
    config.databaseName = configXML.queryserver.souredatamanager.databasename.string
    config.sentimentsDatabaseName = configXML.queryserver.souredatamanager.sentimentsdatabasename.string

    config.user = configXML.queryserver.souredatamanager.user.string
    config.password = configXML.queryserver.souredatamanager.password.string
    config.host = configXML.queryserver.souredatamanager.host.string
    return mySQLSoureDataManager(config, logWriter)
