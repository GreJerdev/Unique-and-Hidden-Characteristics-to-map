from mySQLFeatureDataManager import mySQLFeatureDataManager


def GetSourceDataManager(configXML, logWriter = None):
    config = type('config', (object,), {}) 
    config.databaseName = configXML.queryserver.featuredatamanager.databasename.string
    config.sentimentsDatabaseName = configXML.queryserver.featuredatamanager.sentimentsdatabasename.string

    config.user = configXML.queryserver.featuredatamanager.user.string
    config.password = configXML.queryserver.featuredatamanager.password.string
    config.host = configXML.queryserver.featuredatamanager.host.string
    return mySQLFeatureDataManager(config, logWriter)
