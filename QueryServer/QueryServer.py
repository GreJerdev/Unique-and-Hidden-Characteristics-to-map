from configurationLoader import GetConfiguraton
from SoureDataManager import FactorySoureDataManager
from FeatureDataManager import FactoryFeatureDataManager 
from SentimentPolarity import CalculatePolarity

class QueryServer:

    def __init__(self,config):

        self.__featureDBProvider = FactoryFeatureDataManager.GetFeatureDBProvider(config)
        self.__itemsDBProvider = FactorySoureDataManager.GetSourceDataManager(config)

    def GetItems(self, properties):
        results = self.__itemsDBProvider.GetItemsByCostomFilter(properties)
        itemsIds = list()
        if len(results) > 0:
            itemsIds = [id[1] for id in results[0]]
        return itemsIds
        
    def GetFeature(self, properties):
        items = self.GetItems(properties)
        itemIds = [str(itemId) for itemId in items]
        idsList = str(','.join(itemIds))
        results = self.__featureDBProvider.GetFeatureOfItemsByIds(idsList)
        itemsIds = list()
        if len(results) > 0:
            itemsIds = [row for row in results[0]]
        return itemsIds

        features = None
       
    def GetSimilarItems(self, item):
        pass

    def GetSentimentPolarety(self, type, feature, level):
        pass

    def GetItemsIdByFeatureList(self, featureList):
        pass

    def ComperBetweenItems(self, itemsIdList):
        pass

    def GetFeaturesReview(self, listOFFeature, reviewId):
        pass

    def GetListOfFeatureReviews(self, feature, item):
        pass

    def GetFeaturepolarityInItemReviews(self,featureId,itemId):
        listOfSentences = self.__featureDBProvider.GetFeatureSentimentsByItemId(featureId,itemId)
        polaritylist = self.__CreateListOfpolarityValuesFromSentences(listOfSentences)
        polarity = CalculatePolarity(polaritylist)
        return polarity

    def GetFeaturepolarityInReviews(self,featureId,reviewId):
        listOfSentences = self.__featureDBProvider.GetFeatureSentimentsByReviewId(featureId,reviewId)
        polaritylist = self.__CreateListOfpolarityValuesFromSentences(listOfSentences)
        polarity = CalculatePolarity (polaritylist)
        return polarity

    def GetFeaturepolarityGlobal(self,featureId):
        listOfSentences = self.__featureDBProvider.GetFeatureSentimentsById(featureId)
        polaritylist = self.__CreateListOfpolarityValuesFromSentences(listOfSentences)
        polarity = CalculatePolarity (polaritylist)
        return polarity
    
    def __GetItemReviewsId(self, items):
        pass
    def __CreateListOfpolarityValuesFromSentences(self,listOfSentences):
        polaritylist = list()
        if len(listOfSentences) > 0 and len(listOfSentences[0]) > 0:
            polaritylist = list([pol[2] for pol in listOfSentences[0]])
        return polaritylist
            
server = None

if __name__ == '__main__':
    configXml = GetConfiguraton(None)
     
    server = QueryServer(configXml)
    p = type('point', (object,), {}) 
    p.lat = 33.5760986
    p.lon = -112.0659298
    p.dis = 2
    #print len(server.GetItems(p))
    #print server.GetFeature(p)
    print server.GetFeaturepolarityGlobal(6)
