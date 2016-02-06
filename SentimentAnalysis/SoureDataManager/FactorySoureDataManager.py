from mySQLSoureDataManager import mySQLSoureDataManager


def GetSourceDataManager(configXML, logWriter = None):
    config = type('config', (object,), {}) 
    config.databaseName = configXML.managementunit.souredatamanager.databasename.string
    config.user = configXML.managementunit.souredatamanager.user.string
    config.password = configXML.managementunit.souredatamanager.password.string
    config.host = configXML.managementunit.souredatamanager.host.string
    return mySQLSoureDataManager(config, logWriter)
