from configurationLoader import GetConfiguraton
from SoureDataManager.FactorySoureDataManager import FactorySoureDataManager
from FeatureDataManager.FactoryFeatureDataManager import FactoryFeatureDataManager 

class QueryServer:

    def __init__(self,config):

        self.__featureDBProvider = FactoryFeatureDataManager.GetFeatureDBProvider(config)
        self.__itemsDBProvider = FactorySoureDataManager.GetSourceDataManager(config)

    def GetItems(self, properties):
        return self.__itemsDBProvider.GetItemsByCostomFilter(properties)

    def GetFeature(self, properties):
        items = self.__itemsDBProvider(properties)
        self.__GetItemReviewsId(items)
        features = None
        pass

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
    p.lat = 43.18405
    p.lon = -89.3229659
    p.dis = 10
    print server.GetItems(p)
    
