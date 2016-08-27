from configurationLoader import GetConfiguraton
from SoureDataManager import FactorySoureDataManager
from FeatureDataManager import FactoryFeatureDataManager 
from SentimentPolarity import CalculatePolarity
from CompareItems import CreateCompareTableBetweenItems,CalculateDistance
from ReviewHelper import ReviewHelper
from CommonTypes import Polarity
import QObjects 
import json
import time

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

    def GetItemsFeaturesByItemsIds(self,ItemIds):
        itemsids  = ','.join([str(itemid) for itemid in itemsIdList])
        results = self.__featureDBProvider.GetItemsFeaturesByItemsIds(itemsids)
        results = CreateCompareTableBetweenItems( results)

    def GetFeatureByItemsId(self, itemIds):
        idsList = str(','.join(itemIds))
        results = self.__featureDBProvider.GetFeatureOfItemsByIds(idsList)
        itemsIds = list()
        if len(results) > 0:
            itemsIds = [row for row in results[0]]
        return itemsIds
       
    def GetFeature(self, properties):
        items = self.GetItems(properties)
        itemIds = [str(itemId['id']) for itemId in items]
        idsList = str(','.join(itemIds))
        results = self.__featureDBProvider.GetFeatureOfItemsByIds(idsList)
        itemsIds = list()
        if len(results) > 0:
            itemsIds = [row for row in results[0]]
        return itemsIds

    def GetFeatureInfo(self, featureId):
        itemsSearchResult = self.GetItemsIdByFeatureList([featureId])
        itemIds = [str(item[0]) for item in itemsSearchResult]
        featureInfo = dict()
        featureInfo["info"] = self.GetFeatureStatistics(featureId)
        featureInfo["items"] = itemIds
        featureInfo["reviews"] = self.GetReviewsTextByFeatureId(featureId)
        #for each itemid in itemIds self.GetItemReviewsIdByItemId(itemIds)
        #get all polareties for items and reviews for feature
        #get all reviews text for feature
        return featureInfo

    def GetItemFeaturesAndFeatureSentencesByItemId(self,itemId):
        start_time = time.time()

        itemFeatures = self.__featureDBProvider.GetFeatureOfItemsByIds(itemId)
        featureDict = {feature[1]:feature[0] for feature in itemFeatures[0]}
        featuresSentences = self.__featureDBProvider.GetItemAllItemSentencesWithFeature(itemId)
        featuresNumberOfSentences = self.__featureDBProvider.GetAllFeaturesNumberOfSentences()
        featuresInfo = self.__CreateFeatureInfoForItem(featuresSentences[0])
        result = dict()
        featureOrder = [id[0] for id in sorted([(featureId,len(featuresInfo[featureId]["sentences"])) for featureId in featuresInfo.keys()],key=lambda x: x[1], reverse=True )]
        featureInfo = dict()
        for featurId in featureDict.keys():
            featureInfo[featurId] = dict()
            featureInfo[featurId]["sentences"] = featuresInfo[featurId]["sentences"]
            featureInfo[featurId]["numberOfSentences"] = len(featuresInfo[featurId]["sentences"])
            featureInfo[featurId]["polarity"] = featuresInfo[featurId]["polarity"]
            featureInfo[featurId]["name"] = featureDict[featurId]
            featureInfo[featurId]["positive"] = len([sentences for sentences in featuresInfo[featurId]["sentences"] if sentences["polarity"] > 0 ])
            featureInfo[featurId]["negative"] = len([sentences for sentences in featuresInfo[featurId]["sentences"] if sentences["polarity"] < 0 ])
            featureInfo[featurId]["neutral"] = len([sentences for sentences in featuresInfo[featurId]["sentences"] if sentences["polarity"] == 0 ])

            featureInfo[featurId]["negativePreview"] = [s for s in featuresInfo[featurId]["sentences"] if s["polarity"] < 0 ][0:3]
            featureInfo[featurId]["positivePreview"] = [s for s in featuresInfo[featurId]["sentences"] if s["polarity"] > 0 ][0:3]
            
        result["featureInfo"] = featureInfo
        result["featureOrder"] = featureOrder
        result["frequencyOfMentions"] = featuresNumberOfSentences
        return result
        
    def __CreateFeatureInfoForItem(self,listOfSentences):
        featureListDict = dict()
        featureList = {sentenceRow[6] for sentenceRow in listOfSentences}

        for feature in featureList:
            sentences = [{"text":sentenceRow[1],"polarity":sentenceRow[2],"reviewId":sentenceRow[3], \
                        "tfIdf":sentenceRow[7]} \
                        for sentenceRow in listOfSentences if sentenceRow[6] == feature]
            polarity =  CalculatePolarity([sentenceRow[2] for sentenceRow in listOfSentences if sentenceRow[6] == feature])
            featureListDict[feature] = {"sentences":sentences,"polarity":polarity}
            
        return featureListDict
        
    
    def GetFeatureStatistics(self, featureId):
        allItemSentences = self.__featureDBProvider.GetFeatureReviewsById(featureId)
        statistic = dict()
        setences = [row for row in allItemSentences[0] if str(row[3]) == str(featureId) ]
        items = list(set([row[8] for row in setences]))
        statistic["posSetences"] = len([row for row in setences if row[7] > 0])
        statistic["negSetences"] = len([row for row in setences if row[7] < 0])
        statistic["netSetences"] = len([row for row in setences if row[7] == 0])
        statistic["items"] = len(items)
        statistic["reviews"] = len(set([row[1] for row in setences]))
        statistic["nounsForms"] = list (set([row[5] for row in setences ]))
        statistic["itemSentement"] = {id: CalculatePolarity([row[7] for row in setences if row[8] == id]) for id in items}
        return statistic
        
    def SearchItemsByFeatures(self, listOfFeatures):
        itemsSearchResult = self.GetItemsIdByFeatureList(listOfFeatures)
        itemIds = [str(item[0]) for item in itemsSearchResult]
        idsList = str(','.join(itemIds))
        results = self.__featureDBProvider.GetFeatureOfItemsByIds(idsList)
        features = list()
        if len(results) > 0:
            features = [row for row in results[0] if row[1] in listOfFeatures or str(row[1]) in listOfFeatures]
        result = dict()
        result['items'] = [item  for item in  self.GetAllItems() if str(item['id']) in  itemIds]
        result['features'] = features
        return result

    def GetSimilarItems(self, item):
        percentOfSimilarity = 15
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
                if percent >= percentOfSimilarity:
                    d[i] = results[i]
                
        distance = CreateCompareTableBetweenItems(d)
        
        for itm in distance.keys():
            for featureId in distance[itm]:
                if distance[itm][featureId]['tf_idf'] > 0:
                    distance[itm][featureId]['polarity'] = self.GetFeaturePolarityInItemReviews(featureId,itm)
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

    def GetReviewsTextByFeatureId(self,featureId):
        reviewHalper = ReviewHelper(self.__featureDBProvider)
        return reviewHalper.GetReviewsTextByFeatureId(featureId)

    def GetReviewsTextByFeatureIds(self, featureIdsList):
        reviewHalper = ReviewHelper(self.__featureDBProvider)
        return reviewHalper.GetReviewsTextByFeatureIds(featureIdsList)

    def GetItemsWithFeatures(self,items,features):
        features_items = self.GetItemsIdByFeatureList(features)
        numberOfFeatures = len(features)
        itemsIdWithAllFeatures = [item[0] for item in features_items if item[2] >= numberOfFeatures and str(item[0]) in items]
        itemsIdWithPartOfFeatures = [item[0] for item in features_items if item[2] < numberOfFeatures and str(item[0]) in items]
        reult = dict()
        reult["HaveAllFeatures"] = itemsIdWithAllFeatures
        reult["HavePartOFFeatures"] = itemsIdWithPartOfFeatures
        return reult

    
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

    def bulkTest(self):
        self.__featureDBProvider.BulkTest()

        

server = None
import codecs
if __name__ == '__main__':
    configXml = GetConfiguraton(None)
     
    server = QueryServer(configXml)
    p = type('point', (object,), {}) 
    p.lat = 33.5760986
    p.lon = -112.0659298
    p.dis = 2
    server.GetItemFeaturesAndFeatureSentencesByItemId("130") 
