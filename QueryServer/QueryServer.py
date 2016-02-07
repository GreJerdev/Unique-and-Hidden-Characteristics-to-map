from configurationLoader import GetConfiguraton
from SoureDataManager import FactorySoureDataManager
from FeatureDataManager import FactoryFeatureDataManager 

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

    def __GetItemReviewsId(self, items):
        pass

server = None

if __name__ == '__main__':
    configXml = GetConfiguraton(None)
     
    server = QueryServer(configXml)
    p = type('point', (object,), {}) 
    p.lat = 33.5760986
    p.lon = -112.0659298
    p.dis = 2
    #print len(server.GetItems(p))
    print server.GetFeature(p)
