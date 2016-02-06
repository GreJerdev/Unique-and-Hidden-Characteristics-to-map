from FeatureDataManager import FactoryFeatureDataManager
from SoureDataManager import FactorySoureDataManager 
from FeatureProvider import FactoryFeatureProvider
from configurationLoader import GetConfiguraton
from threading import Lock
from QueueConnector import FactoryQueueConnector
from threading import Thread
import datetime
import json
import time

#cnx = mysql.connector.connect(user='root', 
#password='1qaz2wsx', 
#host='127.0.0.1', database='yelp_challenge')


configXml = GetConfiguraton(None)

featureDataManager = FactoryFeatureDataManager.GetFeatureDataManager(configXml,logWriter=None)
sourceDataManager = FactorySoureDataManager.GetSourceDataManager(configXml, logWriter=None)
featureProvider = FactoryFeatureProvider.GetFeatureProvider(configXml, logWriter=None)
QueueManager = FactoryQueueConnector.GetQueueConnectorClient(configXml, logWriter=None)
lockMain = Lock()

starttime = datetime.datetime.now()

globalData = {}
globalData['totalSendItems'] = 0
globalData['totalreceivedItems'] = 0
globalData['SendProcessEnded'] = False
    
wiatTimeInsecs = 0.05
def PolarityToInt(polarity):
    intPolarity = 0
    if polarity == 'Positive':
        intPolarity = 1
    if polarity == 'Very positive':
        intPolarity = 2
    if polarity == 'Negative':
        intPolarity = -1
    if polarity == 'Very negative':
        intPolarity = -2
    return intPolarity

def SaveFeatureAndSentiment(featureDataManager,featureAndSentiment, reviewid, orderinreview, level):
    orderIndex = 0
    for review in featureAndSentiment:
        features = review['features']
        sentiment = review['sentiment']
        sentence = review['sentence']
        
        id = featureDataManager.AddSentence(sentence,PolarityToInt(sentiment),reviewid, orderIndex)
        orderIndex = orderIndex + 1
        for feature in features:
            featureDataManager.AddFeatureToSentence(feature, id, level, features[feature])    
            

def ProccessItem(itemid):
    ids2 = sourceDataManager.GetListOfReviewIdsByItemId(itemid)
    countOfReviews = len(ids2)
    proccessedReviews = 0
    print ids2
    for reviewId in ids2:
        proccessedReviews = proccessedReviews + 1
        #print ("------------rocessing review %s of %s-------------" %(proccessedReviews,countOfReviews,))
        reviewTextAnsId = sourceDataManager.GetReviewById(reviewId)
        dataToProcess = {}
        dataToProcess['data'] = reviewTextAnsId[0][1]
        dataToProcess['features'] = featureProvider.GetFeatureForItemById(itemid)
        dataToProcess['proccessedReviews'] = proccessedReviews
        dataToProcess['reviewId'] = reviewId
        
        jsonString = json.dumps(dataToProcess)
        QueueManager.addToQueue(jsonString)
        lockMain.acquire()    
        print proccessedReviews,'/',len(ids2), 'item id' ,itemid 
        try:
            globalData['totalSendItems'] = globalData['totalSendItems'] + 1
            
        finally:
            lockMain.release()
        #SP = SentimentProcessUint(configXml)
        #d = SP.ProcessText(dataToProcess)
    
        
def PrintReceivedMsg():
    print '@@@@@@@@@@@@@@@PrintReceivedMsg Enter method'
    while globalData['SendProcessEnded'] == False  or   ((globalData['totalSendItems'] - globalData['totalreceivedItems']) > 0) :
        msg = QueueManager.tryToGet()
        if msg == None:
            time.sleep(wiatTimeInsecs)
        else:
            lockMain.acquire()    
            try:
                globalData['totalreceivedItems'] = globalData['totalreceivedItems'] + 1
                print 'totalSendItems:', globalData['totalreceivedItems'],'/',globalData['totalSendItems'], datetime.datetime.now() - starttime
            finally:
                lockMain.release()
            processedData = json.loads(msg)
            SaveFeatureAndSentiment(featureDataManager, processedData['sentencesWithSentiment'], processedData['reviewId'], processedData['proccessedReviews'], 2 )
    print  '@@@@@@@@@@@@@End of reading loop' ,datetime.datetime.now() - starttime    


if __name__ == '__main__':

    Thread(target=PrintReceivedMsg, args=()).start()

    if featureDataManager.IsDataBaseExist() == False:
        featureDataManager.InitDataBase() 

    ids  = sourceDataManager.GetListOfItems()
    starttime = datetime.datetime.now()

    for id in ids[719:]:
        ProccessItem(id)
        print len(ids), id, datetime.datetime.now() - starttime
    globalData['SendProcessEnded'] = True


