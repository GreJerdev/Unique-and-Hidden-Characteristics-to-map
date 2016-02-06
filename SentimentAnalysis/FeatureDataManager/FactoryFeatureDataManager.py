from mySQLFeatureDataManager import mySQLFeatureDataManager


def GetFeatureDataManager(configXML, logWriter = None):
    config = type('config', (object,), {}) 
    config.name = configXML.managementunit.featuredatamanager.dbschemapostfix.string
    config.user = configXML.managementunit.featuredatamanager.user.string
    config.password = configXML.managementunit.featuredatamanager.password.string
    config.host = configXML.managementunit.featuredatamanager.host.string
    return mySQLFeatureDataManager(config, logWriter)


