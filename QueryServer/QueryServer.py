from configurationLoader import GetConfiguraton
from SoureDataManager import FactorySoureDataManager
from FeatureDataManager import FactoryFeatureDataManager 
from SentimentPolarity import CalculatePolarity
from CompareItems import CreateCompareTableBetweenItems,CalculateDistance
from ReviewHelper import ReviewHelper
from CommonTypes import Polarity
import QObjects 
import json

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
        results = self.__featureDBProvider.GetFeatureInfoByItemId(ItemId)
       
        itemsIds = list()
        if len(results) > 0:
            itemsIds = [{'text':row[0],'id':row[1],'polarity':self.GetFeaturePolarityInItemReviews(row[1],ItemId),'tf_idf':row[2]} for row in results[0]]
        return itemsIds
        
    def GetFeature(self, properties):
        items = self.GetItems(properties)
        itemIds = [str(itemId['id']) for itemId in items]
        idsList = str(','.join(itemIds))
        results = self.__featureDBProvider.GetFeatureOfItemsByIds(idsList)
        itemsIds = list()
        if len(results) > 0:
            itemsIds = [row for row in results[0]]
        print len(itemsIds)
        return itemsIds

       
    def GetSimilarItems(self, item):
        results = self.__featureDBProvider.GetItemsFeaturesByItemsIds('')
        similarItems = dict()
        distanceDict = dict()
        d = dict()
        d[item] = results[item]
        itemFeaturesIds = d[item].keys()
        for i in results.keys():
            numOfItems = len(results[i].keys())
            if numOfItems > 0:
                numOfFeaturesNotInItem = len(set(results[i].keys()) - set(itemFeaturesIds))
                percent = 100 - (100*numOfFeaturesNotInItem)/ numOfItems 
                if percent > 7:
                    print percent
                    d[i] = results[i]
                
        distance = CreateCompareTableBetweenItems(d)
        for i in d.keys():
            similarItems[i] = dict()
            distanceDict[i] = CalculateDistance(distance[i],distance[item])	
            similarItems[i]['distance'] = distanceDict[i]
            similarItems[i]['features'] = distance[i]
        print len(similarItems)
        return similarItems

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

    def GetItemsWithFeatures(self,items,features):
        features_items = self.GetItemsIdByFeatureList(features)
      
        itemsId = [item[0] for item in features_items]
        itemsAsInt = [int(item) for item in items if len(item) > 0]
        result = [item for item in itemsAsInt if item in itemsId]
        return result

    def GetItemReview(reviewId):
        GetReviewsTextByItemIdAndFeatureIds
        pass
    
    def GetAllItems(self):
        results = self.__itemsDBProvider.GetAllItems()
        itemsIds = [QObjects.Item_to_dict(id) for id in results[0]]
        return itemsIds

    def GetAllFeatures(self):
        itemsIds = list()
        results = self.__featureDBProvider.GetAllFeatures()
        if len(results) > 0:
            itemsIds = [row for row in results[0]]
        print len(itemsIds)
        return itemsIds

    def GetReviewSentencesById(self, reviewId):
        reviewHalper = ReviewHelper(self.__featureDBProvider)
        results = reviewHalper.GetReviewTestByReviewId(reviewId) 
        return results

    def GetReviewsTextByItemId(self, itemId):
        reviewHalper = ReviewHelper(self.__featureDBProvider)
        results = reviewHalper.GetReviewsTextByItemId(itemId) 
        return results 
    
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

    arr = [9620,6127,6185,7739,12450,237,5950,280,4230,9793,222,12428,5621,5568,6206,13781,245,2243,2256,6201,13491,2254,11619,10088,226,3742,292,4488,13915]
    feat = [61]
    #server.GetItemsWithFeatures(arr,feat)
    #itemFeatures = [feature[1] for feature in server.GetFeatureByItemId('131,')]
    #print itemFeatures
    #print server.GetReviewsTextByItemIdAndFeatureIds('131',itemFeatures)
    review = server.GetReviewsTextByItemId('130')
     
    
    #print server.GetAllItems()
    #server.testDB()
    #ReviewHelper
    #print len(server.GetFeature(p))
    #print server.GetFeature(p)
    #print server.GetFeaturepolarityGlobal(6)
    #distance =  server.GetSimilarItems(2406)
    #print server.ComperBetweenItems([2406,5724])
    #print server.GetReviewsTextByItemIdAndFeatureIds([130],['1390','225'])
    #with codecs.open("d:/yop.xml", "w", encoding="utf-8") as f:
    #    for r in  server.GetReviewsTextByFeatureIds([133,131,132,130,141,1,2,3,4,1,54,34,65,34,234,654,34,7,6,87,80,87,67,655,887,766,996,455]):
    #        f.write(r)

    
  
