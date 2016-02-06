import mysql.connector
from BaseSoureDataManager import BaseSoureDataManager
from mysql.connector import Error

class mySQLSoureDataManager(BaseSoureDataManager):
 
    def __init__(self, configuration,logWriter=None):
        self._Configuration = configuration
        self._logWriter = logWriter

    def WriteLog(self, logLevel, message):
        if not(self._logWriter is None) :
           self._logWriter.WriteLog(logLevel,messge)
        else:
           print(message)

    def GetItemsByCostomFilter(self, params):
        args = (params.lat,params.lon,params.dis)
        return self.__CallProcWithOutParameter('usp_get_restorans_by_location',args,name)

    def GetFeatureOfItemsByIds(self, itemsIds):
        pass

    def GetFeatureSentimentsByItemId(self, itemId, featureId):
        pass

    def GetItemsIdByFeatureList(self, featureIds):
        pass
    
        
    def __ExecuteQuery(self, query, args=None):
        results = list()
        try:
            cnx = mysql.connector.connect(user=self._Configuration.user, 
            password=self._Configuration.password, 
            host=self._Configuration.host, database=self._Configuration.databaseName)
            cursor = cnx.cursor()
            #self.WriteLog(3,query)
            #self.WriteLog(3,args)
            cursor.execute(query,args)
            results = list(cursor)
            cnx.commit()
           
        except Error as e:
            self.WriteLog(4, e) 
        finally:
            cursor.close()
            cnx.close()
       
        return results
    
    def __CallProcWithOutParameter(self,procName,args,name):
        retVals = None
        try:
            cnx = mysql.connector.connect(user=self._Configuration.user, 
            password=self._Configuration.password, 
            host=self._Configuration.host, database=self._Configuration.databaseName)
            cursor = cnx.cursor()
            cursor = conn.cursor()
 
            result_args = cursor.callproc(procName, args)
            conn.commit()
            retVals = result_args
 
        except Error as e:
            self.WriteLog(4, e) 
             
        finally:
            cursor.close()
            conn.close()
        return retVals

   
    
            

            
