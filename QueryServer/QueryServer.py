from configurationLoader import GetConfiguraton
from SoureDataManager import FactorySoureDataManager
from FeatureDataManager import FactoryFeatureDataManager 
from SentimentPolarity import CalculatePolarity
from CompareItems import CreateCompareTableBetweenItems,CalculateDistance
from ReviewHelper import ReviewHelper
from CommonTypes import Polarity
import QObjects 

class QueryServer:

    def __init__(self,config):

        self.__featureDBProvider = FactoryFeatureDataManager.GetFeatureDBProvider(config)
        self.__itemsDBProvider = FactorySoureDataManager.GetSourceDataManager(config)

    def GetItems(self, properties):
        results = self.__itemsDBProvider.GetItemsByCostomFilter(properties)
        itemsIds = list()
        if len(results) > 0:
            itemsIds = [QObjects.Item_to_dict(id) for id in results[0]]
        return itemsIds

    def GetFeatureByItemId(self, ItemId):
        results = self.__featureDBProvider.GetFeatureOfItemsByIds(ItemId)
        itemsIds = list()
        if len(results) > 0:
            itemsIds = [row for row in results[0]]
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

       
    def GetSimilarItems(self, item):
        results = self.__featureDBProvider.GetItemsFeaturesByItemsIds('')
        distanceDict = dict()
        for i in results.keys():
            print i , item
            if(not i == int(item)):
                d = {}
                d[i] = results[i]
                d[item] = results[item]
                distance = CreateCompareTableBetweenItems(d)
                distanceDict[i] = CalculateDistance(distance[i],distance[item])
        return distanceDict

    def GetItemsIdByFeatureList(self, featureList):
        featuresid = ','.join([str(feature) for feature in featureList])
        results = self.__featureDBProvider.GetItemsIdByFeatureList(featuresid)
        itemsIds = list()
        if len(results) > 0:
            itemsIds = [row for row in results[0]]
        return itemsIds

    def ComperBetweenItems(self, itemsIdList):
        itemsids  = ','.join([str(itemid) for itemid in itemsIdList])
        results = self.__featureDBProvider.GetItemsFeaturesByItemsIds(itemsids)
        results = CreateCompareTableBetweenItems( results)

        return results

    def GetItemReviewsIdByItemId(self, itemId):     
        results = self.__featureDBProvider.GetItemReviewsIdByItemId(itemId)
        return results

    def GetFeaturePolarityInItemReviews(self,featureId,itemId):
        listOfSentences = self.__featureDBProvider.GetFeatureSentimentsByItemId(featureId,itemId)
        polaritylist = self.__CreateListOfpolarityValuesFromSentences(listOfSentences)
        polarity = CalculatePolarity(polaritylist)
        return polarity

    def GetFeaturePolarityInReviews(self,featureId,reviewId):
        listOfSentences = self.__featureDBProvider.GetFeatureSentimentsByReviewId(featureId,reviewId)
        polaritylist = self.__CreateListOfpolarityValuesFromSentences(listOfSentences)
        polarity = CalculatePolarity (polaritylist)
        return polarity

    def GetFeaturePolarityGlobal(self,featureId):
        listOfSentences = self.__featureDBProvider.GetFeatureSentimentsById(featureId)
        polaritylist = self.__CreateListOfpolarityValuesFromSentences(listOfSentences)
        polarity = CalculatePolarity (polaritylist)
        return polarity

    def GetReviewsTextByItemIdAndFeatureIds(self,itemId, featureIdsList, polarity = Polarity.ALL):
        reviewHalper = ReviewHelper(self.__featureDBProvider)
        return reviewHalper.GetReviewsTextByItemIdAndFeatureIds(itemId, featureIdsList, polarity = Polarity.ALL)

    def GetReviewsTextByFeatureIds(self, featureIdsList):
        reviewHalper = ReviewHelper(self.__featureDBProvider)
        return reviewHalper.GetReviewsTextByFeatureIds(featureIdsList)

    def __GetItemReviewsId(self, items):
        pass
    
    def __CreateListOfpolarityValuesFromSentences(self,listOfSentences):
        polaritylist = list()
        if len(listOfSentences) > 0 and len(listOfSentences[0]) > 0:
            polaritylist = list([pol[2] for pol in listOfSentences[0]])
        return polaritylist


server = None
import codecs
if __name__ == '__main__':
    configXml = GetConfiguraton(None)
     
    server = QueryServer(configXml)
    p = type('point', (object,), {}) 
    p.lat = 33.5760986
    p.lon = -112.0659298
    p.dis = 2
    #server.testDB()
    #ReviewHelper
    #print len(server.GetFeature(p))
    #print server.GetFeature(p)
    #print server.GetFeaturepolarityGlobal(6)
    #distance =  server.GetSimilarItems(2406)
    #print server.ComperBetweenItems([2406,5724])
    #print server.GetReviewsTextByItemIdAndFeatureIds([130],['1390','225'])
    with codecs.open("d:/yop.xml", "w", encoding="utf-8") as f:
        for r in  server.GetReviewsTextByFeatureIds([133,131,132,130,141,1,2,3,4,1,54,34,65,34,234,654,34,7,6,87,80,87,67,655,887,766,996,455]):
            f.write(r)

    
  
