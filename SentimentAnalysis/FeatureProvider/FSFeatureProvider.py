import shelve
import sys
from os import listdir
from os.path import isfile, join
from BaseFeatureProvider import BaseFeatureProvider

class FSFeatureProvider(BaseFeatureProvider):
 
    def __init__(self, configuration, logWriter=None):
        BaseFeatureProvider.__init__(self, configuration, logWriter)
        self._Configuration = configuration 
     
    def GetFeatureForItemById(self, id):
        pathTodateFile = join(self._Configuration.path,str(id),'tfidf.db')
        #self.__WriteLog(3,pathTodateFile)    
        retVal = {}
        try:
            #self.__WriteLog(3,"open shelve file")
            retVal = shelve.open(pathTodateFile)["data"]
        except:
            self.__WriteLog(5, "Unexpected error: %s" %( sys.exc_info()[0],))
        return retVal
    
    def __WriteLog(self, logLevel, message):
        if not(self._logWriter is None):
           _logWriter.WriteLog(logLevel,messge)
        else:
           print(message)





