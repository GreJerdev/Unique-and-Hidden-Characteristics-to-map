import mysql.connector
from mysql.connector import Error
from BaseFeatureDataManager import BaseFeatureDataManager

class mySQLFeatureDataManager(BaseFeatureDataManager):
 
    def __init__(self, configuration,logWriter=None):
        self._Configuration = configuration
        self._logWriter = logWriter

    def WriteLog(self, logLevel, message):
        if not(self._logWriter is None) :
           _logWriter.WriteLog(logLevel,messge)
        else:
           print(message)
    
    def InitDataBase(self):
        name = self._Configuration.name
        self.__CreateDB(name)
        self.__CreateTables(name)
        self.__CreateSP(name)  

    def IsDataBaseExist(self):
        name = self._Configuration.name
        databaseName = (str.format("sentiments_and_feature_for_{0}",name),)
        sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s"
        results = self.ExecuteSelectQuery( query=sql, args=databaseName)
        return len(results) > 0 
            
    def __CreateDB(self, name):
        databaseName = str.format("sentiments_and_feature_for_{0}",name);
        sql = str.format("CREATE DATABASE {0}",databaseName)
        self.WriteLog(3,sql)
        cnx = mysql.connector.connect(user=self._Configuration.user, 
        password = self._Configuration.password, 
        host = self._Configuration.host)
        cursor = cnx.cursor()
        self.WriteLog(3,sql)
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        cnx.close() 

        
        
    def __CreateTables(self,name):
        createFeatureTable = str.format("CREATE TABLE feature_{0}(id int(6) NOT NULL AUTO_INCREMENT, feature VARCHAR(50) NOT NULL, PRIMARY KEY (id));",name)
        createSentencesTable = str.format("CREATE TABLE sentences_{0}(id int(6) NOT NULL AUTO_INCREMENT, sentence_text text NOT NULL, polarity int(6)NOT NULL, review_id int(6), order_in_review int(6), PRIMARY KEY (id));",name)
        createFeatureToSentencesTable = str.format("CREATE TABLE feature_to_sentences_{0}(feature_id int(6) NOT NULL, sentences_id int(6) NOT NULL, level int(6) NOT NULL, tf_idf DOUBLE(7,5) );",name)
        databaseName = str.format("sentiments_and_feature_for_{0}",name);
        self.ExecuteQuery(createFeatureTable,databaseName=databaseName)
        self.ExecuteQuery(createSentencesTable,databaseName=databaseName)
        self.ExecuteQuery(createFeatureToSentencesTable,databaseName=databaseName)
         
    def __CreateSP(self,name):
        #Drop procedure IF EXISTS csp_add_feature_to_sentence $$
        add_csp_add_feature_to_sentence = str.format("""  
Create procedure csp_add_feature_to_sentence(feature_value varchar(50), sentenceid int(6),feature_level int(6),feature_tf_idf DOUBLE(7,5))
BEGIN

DECLARE  featureId int(6);
SET @featureId = (SELECT id from feature_{0}
where feature like feature_value LIMIT 1);
SELECT @featureId;

if @featureId IS NULL THEN

	insert into feature_{0} (feature) values(feature_value);
    SET @featureId = (SELECT LAST_INSERT_ID());
END IF;

insert into feature_to_sentences_{0} (feature_id, sentences_id, level, tf_idf)
values(@featureId, sentenceid, feature_level, feature_tf_idf);

END ;
""",name)
        #Drop procedure IF EXISTS csp_add_sentence $$
        add_csp_add_sentence = str.format("""                                                    

Create procedure csp_add_sentence(sentencetext text, sentencepolarity int(6),reviewid int(6), orderinreview int(6),OUT sentence_id int(6) )
BEGIN
	insert into sentences_{0} (sentence_text,polarity,review_id,order_in_review) 
    values(sentencetext,sentencepolarity,reviewid,orderinreview);
    SET sentence_id = (SELECT LAST_INSERT_ID());

END ;

 """,name)
        databaseName = str.format("sentiments_and_feature_for_{0}",name);
        self.ExecuteQuery(add_csp_add_feature_to_sentence,databaseName=databaseName)
        self.ExecuteQuery(add_csp_add_sentence,databaseName=databaseName)
        
    def ExecuteQuery(self,query,databaseName=None):
        try:
            cnx = mysql.connector.connect(user=self._Configuration.user, 
            password= self._Configuration.password, 
            host= self._Configuration.host, database=databaseName)
            cursor = cnx.cursor()
            self.WriteLog(3,query)
            cursor.execute(query)
            cnx.commit()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            cnx.close()
            
    def ExecuteSelectQuery(self, query, args=None, databaseName=None):
        results = list()
        try:
            cnx = mysql.connector.connect(user=self._Configuration.user, 
            password=self._Configuration.password, 
            host=self._Configuration.host, database=databaseName)
            cursor = cnx.cursor()
            self.WriteLog(3,query)
            self.WriteLog(3,args)
            cursor.execute(query,args)
            results = list(cursor)
            cnx.commit()
           
        except Error as e:
            self.WriteLog(4, e) 
        finally:
            cursor.close()
            cnx.close()
       
        return results        

    def CallProc(self,procName,args,name):
        retVals = None
        try:
            databaseName = str.format("sentiments_and_feature_for_{0}",name);
            conn = mysql.connector.connect(user=self._Configuration.user, 
            password= self._Configuration.password, 
            host = self._Configuration.host, database=databaseName)
            cursor = conn.cursor()
 
            result_args = cursor.callproc(procName, args)
            conn.commit()
            retVals = result_args
 
        except Error as e:
            print(e)
 
        finally:
            cursor.close()
            conn.close()
        return retVals
    
    def AddSentence(self,sentence,sentencepolarity,reviewid,orderinreview):
        name = self._Configuration.name
        new_sentence_id = 0
        asgs = [sentence, sentencepolarity, reviewid, orderinreview, new_sentence_id]
        retvals = self.CallProc('csp_add_sentence', asgs, name)
        return retvals[4]
        
    def AddFeatureToSentence(self,feature_value,sentenceid, feature_level,feature_tf_idf):
        name = self._Configuration.name
        new_sentence_id = 0
        asgs = [feature_value, sentenceid, feature_level, feature_tf_idf]
        retvals = self.CallProc('csp_add_feature_to_sentence', asgs, name)
            
'''CREATE DEFINER=`root`@`localhost` PROCEDURE `csp_get_features_by_items_id`(list_of_items_ids varchar(250) )
BEGIN

select feature,feature_rest_db.id as 'id',count(1) as 'count'
from sentences_rest_db inner join feature_to_sentences_rest_db
on sentences_id = sentences_rest_db.id
inner join feature_rest_db on
feature_id = feature_rest_db.id
where FIND_IN_SET(sentences_rest_db.restaurant_id, list_of_items_ids)
group by feature,feature_rest_db.id
order by count(1) ;

END'''
            
