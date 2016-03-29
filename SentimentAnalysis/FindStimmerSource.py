from FeatureDataManager import FactoryFeatureDataManager
from SoureDataManager import FactorySoureDataManager 
from FeatureProvider import FactoryFeatureProvider
from configurationLoader import GetConfiguraton
import nltk
from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger()
import mysql.connector
from mysql.connector import Error
from nltk.stem import *

stemmer = PorterStemmer()
tagset = None
tokens = nltk.word_tokenize('We sampled the chicken, lamb, and filet kabobs.')
tags = nltk.tag._pos_tag(tokens, tagset, tagger)
cursor = None
retVals = None

def updateData(f_id,s_id,index,feature):
    try:
        conn = mysql.connector.connect(user='root', 
        password='1qaz2wsx' , 
        host = '127.0.0.1', database='sentiments_and_feature_for_rest_db')
        cursor = conn.cursor()
        print "update feature_to_sentences_rest_db set feature_as_in_sentencesl = '" +feature+"',feature_index_insentences = " +str(index)+" where feature_id = " + str(f_id)+" and sentences_id = "+ str(s_id)
        cursor.execute("update feature_to_sentences_rest_db set feature_as_in_sentencesl = '" +feature+"',feature_index_insentences = " +str(index)+" where feature_id = " + str(f_id)+" and sentences_id = "+ str(s_id))
        conn.commit() 
    except Error as e:
        print('error:', e)
    finally:
        cursor.close()
        conn.close()

try:
    conn = mysql.connector.connect(user='root', 
    password='1qaz2wsx' , 
    host = '127.0.0.1', database='sentiments_and_feature_for_rest_db')
    cursor = conn.cursor()
    cursor.execute('''select feature_to_sentences_rest_db.feature_id,feature_to_sentences_rest_db.sentences_id,  feature_rest_db.feature, sentence_text
from feature_to_sentences_rest_db inner join sentences_rest_db
on feature_to_sentences_rest_db.sentences_id = sentences_rest_db.id
inner join feature_rest_db on feature_rest_db.id = feature_to_sentences_rest_db.feature_id
where feature_as_in_sentencesl is null;
''',None)
    
    retVals = list(cursor)
    conn.commit()         
except Error as e:
   
    print('error:', e)
             
finally:
    cursor.close()
    conn.close()

total = len(retVals)
j = 0
for row in retVals:
    #print j,'/',total
    sent_id = row[1]
    feat_id = row[0]
    stmmer = row[2]
    test = row[3]
    tokens = nltk.word_tokenize(test.replace('.',' ').replace(',',' '))
    tags = nltk.tag._pos_tag(tokens, tagset, tagger)
    i = 0
    print "----------------------"
    for tag in tags:
          
        s = stemmer.stem(tag[0])
        print s,stmmer
        if stmmer == s:
            print 'bingo-->',s,stmmer
            updateData(feat_id,sent_id,i,tag[0])           
        i = i + 1  
    #print row[0],row[1],tags
    j = j + 1
