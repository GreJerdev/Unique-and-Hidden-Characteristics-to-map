import mysql.connector
from BaseFeatureDataManager import BaseFeatureDataManager
from mysql.connector import Error

class mySQLFeatureDataManager(BaseFeatureDataManager):
 
    def __init__(self, configuration,logWriter=None):
        self._Configuration = configuration
        self._logWriter = logWriter

    def WriteLog(self, logLevel, message):
        if not(self._logWriter is None) :
           self._logWriter.WriteLog(logLevel,messge)
        else:
           print(message)

    def GetItemsByCostomFilter(self, params):
        pass

    def GetFeatureOfItemsByIds(self, itemsIds):
        args = (itemsIds,)
        return self.__CallProcWithParameter('csp_get_features_by_items_id',args)

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

   
    
            

            
