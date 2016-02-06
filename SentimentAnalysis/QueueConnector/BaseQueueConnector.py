

class BaseQueueConnector(object):
 
    def __init__(self, configuration,logWriter=None):
        self._Configuration = configuration
        self._logWriter = logWriter

    def addToQueue(self, strdata):
        pass
    
    def tryToGet(self):
        pass
    
    def __WriteLog(self, logLevel, message):
        if not(self._logWriter is None) :
           _logWriter.WriteLog(logLevel,messge)
        else:
           print(message)
    
    
