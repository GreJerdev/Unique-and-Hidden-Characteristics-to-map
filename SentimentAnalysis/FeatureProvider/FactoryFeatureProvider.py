from FSFeatureProvider import FSFeatureProvider

def GetFeatureProvider(configXML, logWriter = None):
    config = type('config', (object,), {}) 
    config.path = configXML.managementunit.featureprovider.path.string
    return FSFeatureProvider(config, logWriter)
