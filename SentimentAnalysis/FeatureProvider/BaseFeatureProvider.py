

class BaseFeatureProvider(object):
 
    def __init__(self, configuration,logWriter=None):
        self._Configuration = configuration
        self._logWriter = logWriter

    def GetFeatureForItemById(self, id):
        pass
    
    def __WriteLog(self, logLevel, message):
        if not(self._logWriter is None) :
           _logWriter.WriteLog(logLevel,messge)
        else:
           print(message)
    
    
