import mysql.connector
from BaseFeatureDataManager import BaseFeatureDataManager
from mysql.connector import Error

class Command(object):

    def __init__(self,procName = None, args = None):
        self._procName = procName
        self._args = args
    
    @property
    def ProcName(self):
        return self._procName

    @ProcName.setter
    def ProcName(self, value):
        self._procName = value
        print self._procName
        
    @property
    def Args(self):
        return self._args

    @Args.setter
    def Args (self, value):
        self._args =  value
        print self._args    

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

    def GetItemReviewsIdByItemId(self, itemId ):
        args = (itemId,)
        return self.__CallProcWithParameter('csp_get_item_reviews_id_by_item_id',args)

    def GetFeatureInfoByItemId(self, itemId ):
        args = (itemId,)
        return self.__CallProcWithParameter('csp_get_features_info_by_item_id',args)

    def GetItemsIdByFeatureList(self, featureIds):
        args = (featureIds,)
        return self.__CallProcWithParameter('csp_get_items_by_featuresids',args)

    def GetFeatureOfItemsByIds(self, itemsIds):
        args = (itemsIds,)
        return self.__CallProcWithParameter('csp_get_features_by_items_id',args)
    
    def GetFeatureSentenceByReviewId(self, featureId, reviewId):
        args = (featureId, reviewId,)
        return self.__CallProcWithParameter('csp_get_feature_sentence_by_review_id',args)

    def GetFeatureSentimentsById(self, featureId):
        args = (featureId,)
        return self.__CallProcWithParameter('csp_get_feature_sentence_feature_id',args)

    def GetFeatureReviewsById(self, featureId):
        args = (featureId,)
        return self.__CallProcWithParameter('csp_get_reviews_by_feature_id',args)
    
    def GetItemsFeaturesByItemsIds(self, itemsIds):
        args = (itemsIds,)
        result = {}
        queryResult = self.__CallProcWithParameter('csp_get_items_features',args)
        if len(queryResult) > 0:
            itemsIds = [row for row in queryResult[0]]
            for item in itemsIds:
                result[item[0]] =  { int(f.split('|')[0]):  {'tf_idf':float(f.split('|')[1]),'text':f.split('|')[2],'polarity':0}for f in item[1].split(',')}
               
        return result

    def GetReviewsSentencesByFeatureIds(self, featuresIdsList):
        featuresids = ','.join([str(feature) for feature in featuresIdsList])
        args = (featuresids,)
        print args
        return self.__CallProcWithParameter('csp_get_reviews_sentences_by_features_ids',args)

    def GetReviewsSentencesByItemsAndFeatureIds(self,itemsIdsList, featuresIdsList):
        featuresids = ','.join([str(feature) for feature in featuresIdsList])
        itemsids = ','.join([str(itemid) for itemid in itemsIdsList])
        args = (itemsids,featuresids,)
        return self.__CallProcWithParameter('csp_get_reviews_sentences_by_items_and_features_ids',args)

    def GetReviewSentencesById(self,reviewId):
        args = (reviewId,)
        return self.__CallProcWithParameter('csp_get_review_sentences_by_id',args)
        
    def GetFeatureAsIsInSentences(self,sentencesIdsList, featuresIdsList):
        featuresids = ','.join([str(feature) for feature in featuresIdsList])
        sentencesids = ','.join([str(sentencesid) for sentencesid in sentencesIdsList])
        args = (sentencesids,featuresids,)
        result = {}
        queryResult = self.__CallProcWithParameter('csp_get_feature_as_is_in_sentences',args)
        if len(queryResult) > 0:
            result = { (row[0],row[1]): row[4] for row in queryResult[0]}
        return result

    def GetAllFeatures(self):
        return self.__CallProcWithParameter('csp_get_all_features',())

    def GetReviewSentencesByReviewId(self, id):
        return self.__CallProcWithParameter('csp_get_review_sentences',(id,))

    def GetReviewSentencesByItemId(self, id):
        return self.__CallProcWithParameter('csp_get_reviews_sentences_by_item_id',(id,))

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

    def __CallProcWithParameterBulk(self,listCommandsAndParameters):
        retVals = list()
        try:
            conn = mysql.connector.connect(user=self._Configuration.user, 
            password=self._Configuration.password, 
            host=self._Configuration.host, database=self._Configuration.databaseName)
            cursor = conn.cursor()

            for commandAndParameters in listCommandsAndParameters:
                print commandAndParameters.ProcName, commandAndParameters.Args
                cursor.callproc(commandAndParameters.ProcName, commandAndParameters.Args)
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

    def BulkTest(self):
        listCP = list()
        listCP.append(Command('csp_get_reviews_by_feature_id',(1,)))
        listCP.append(Command('csp_get_reviews_by_feature_id',(2,)))
        listCP.append(Command('csp_get_reviews_by_feature_id',(3,)))
        listCP.append(Command('csp_get_reviews_by_feature_id',(4,)))
        for table in self.__CallProcWithParameterBulk(listCP):
            print len(table)
    
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

   
    
            

            
