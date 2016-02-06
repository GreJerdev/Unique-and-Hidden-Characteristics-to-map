import json
import sys
from SentimentRecognition import FactorySentimentRecognition
from FeatureRecognition import FactoryFeatureRecognition
from configurationLoader import GetConfiguraton
from QueueConnector import FactoryQueueConnector
from configurationLoader import GetConfiguraton


class SentimentProcessUint() :

    def __init__(self,configXml):
        self.__sentimentRecognition = FactorySentimentRecognition.GetSentimentRecognition(configXml)
        self.__featureRecognition = FactoryFeatureRecognition.GetFeatureRecognition(configXml)

    def ProcessText(self,jsonDataToProcess):

        print 'Process begin'
        dataToProcess = json.loads(jsonDataToProcess)
        sentencesWithSentiment = json.loads(self.__GetTextSentiment(dataToProcess['data']),strict=False)
        for sentenceInfo in sentencesWithSentiment:
            featuresList = self.__GetTextFeature(sentenceInfo['sentence'],dataToProcess['features'].keys())
            sentenceInfo['features'] = {feature:dataToProcess['features'][feature]for feature in featuresList}
        processedData = {}
        processedData['sentencesWithSentiment'] = sentencesWithSentiment
        processedData['proccessedReviews'] = dataToProcess['proccessedReviews']
        processedData['reviewId'] = dataToProcess['reviewId']
        print 'process end'
        return json.dumps(processedData)
    
        
    def __GetTextSentiment(self,text):
        retVal = {}
        try:
            retVal = self.__sentimentRecognition.GetSentiments(text)
        except:
            print "Unexpected error:", sys.exc_info()[0]
        return retVal

    def __GetTextFeature(self,text,listOfFeatures):
        retVal = {}
        try:
            retVal = self.__featureRecognition.GetFeatures(text, listOfFeatures)
        except:
            print "Unexpected error:", sys.exc_info()[0]
        return retVal
if __name__ == '__main__':

    configXml = GetConfiguraton(None)
    sentimentProcessUint = SentimentProcessUint(configXml)
    Server = FactoryQueueConnector.GetQueueConnectorServer(configXml, sentimentProcessUint.ProcessText,logWriter=None)
