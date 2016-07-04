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
        return self.__CallProcWithParameter('usp_get_restorans_by_location',args)

    def GetFeatureOfItemsByIds(self, itemsIds):
        pass

    def GetFeatureSentimentsByItemId(self, itemId, featureId):
        pass

    def GetItemsIdByFeatureList(self, featureIds):
        pass
        
    def GetAllItems(self):
        return self.__CallProcWithParameter('usp_get_all_restorans',())
       
    def __ExecuteQuery(self, query, args=None):
        results = list()
        try:
            cnx = mysql.connector.connect(user=self._Configuration.user, 
            password=self._Configuration.password, 
            host=self._Configuration.host, database=self._Configuration.databaseName)
            cursor = cnx.cursor()
            cursor.execute(query,args)
            results = list(cursor)
            cnx.commit()
           
        except Error as e:
            self.WriteLog(4, e) 
        finally:
            cursor.close()
            cnx.close()
       
        return results
    
    def __CallProcWithParameter(self,procName,args):
        retVals = list()
        try:
            conn = mysql.connector.connect(user=self._Configuration.user, 
            password=self._Configuration.password, 
            host=self._Configuration.host, database=self._Configuration.databaseName)
            cursor = conn.cursor()
 
            cursor.callproc(procName, args)
            cursor.fetchone()
            results = cursor.stored_results()
            
            for result in results:
                table = list()
                for row in result:
                    table.append(row)
                retVals.append(table)
                
            conn.commit()
        except Error as e:
            self.WriteLog(4, e) 
             
        finally:
            cursor.close()
            conn.close()
        return retVals

   
    
            

            
