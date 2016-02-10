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
    def GetFeatureSentimentsByItemId(self, featureId, itemId ):
        args = (featureId,itemId,)
        return self.__CallProcWithParameter('csp_get_feature_sentence_by_item_id',args)

    def GetItemsIdByFeatureList(self, featureIds):
        pass

    def GetFeatureOfItemsByIds(self, itemsIds):
        args = (itemsIds,)
        return self.__CallProcWithParameter('csp_get_features_by_items_id',args)
    
    def  GetFeatureSentimentsByReviewId(self, featureId, reviewId):
        args = (featureId, reviewId,)
        return self.__CallProcWithParameter('csp_get_feature_sentence_by_review_id',args)

    def GetFeatureSentimentsById(self, featureId):
        args = (featureId,)
        return self.__CallProcWithParameter('csp_get_feature_sentence_feature_id',args)
        
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

   
    
            

            
