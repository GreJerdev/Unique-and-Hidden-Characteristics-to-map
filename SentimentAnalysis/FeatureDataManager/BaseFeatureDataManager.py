import mysql.connector
from mysql.connector import Error

class BaseFeatureDataManager(object):
 
    def __init__(self, configuration,logWriter=None):
        self._Configuration = configuration
        self._logWriter = logWriter

    def WriteLog(self, logLevel, message):
        if not(self._logWriter is None) :
           _logWriter.WriteLog(logLevel,messge)
        else:
           print(message)
           
    def InitDataBase(self):
        pass
    
    def ExecuteQuery(self,query,databaseName=None):
        pass

    def CallProc(self,procName,args,name):
        pass
    
    def AddSentence(self,sentence,sentencepolarity,reviewid,orderinreview):
        pass
        
    def AddFeatureToSentence(self,feature_value,sentenceid,feature_tf_idf):
        pass
            

            
