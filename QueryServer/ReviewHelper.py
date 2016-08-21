from SentimentPolarity import CalculatePolarity
from CommonTypes import Polarity
from collections import OrderedDict
from QObjects import SentenceMember, Sentence, Review, Item
import time

class ReviewHelper(object):
    __featureProvider = None
    def __init__(self, featureProvider):
        self.__featureProvider = featureProvider
            
       
    def GetReviewsSentencesByFeatureIds(self, featureidsList):
        
        return self.__featureProvider.GetReviewsSentencesByFeatureIds(featureidsList)[0]

    def GetReviewsTextByFeatureId(self, featureId):
        #1.get all reviews sentences
        allItemSentences = self.__featureProvider.GetFeatureReviewsById(featureId)
        #2.get all items ids
        print 1
        itemidsList = set([sentence[8] for sentence in allItemSentences[0]])
        featureReviews = {}
        for itemid in itemidsList:
            itemSentences = [sentence  for sentence in allItemSentences[0] if sentence[8] == itemid]
            featureReviews[itemid] = self.__GetItemObject(itemid, itemSentences)
        return featureReviews
        
    def GetReviewsTextByFeatureIds(self, featureIdsList, polarity = Polarity.ALL):
        listOfSentences = self.__featureProvider.GetReviewsSentencesByFeatureIds(featureIdsList)
        return self.MergeToReview(listOfSentences[0], featureIdsList)

    def GetReviewsTextByItemId(self, itemId):
        listOfSentences = self.__featureProvider.GetReviewSentencesByItemId(itemId)
        return self.__GetItemObject(itemId, listOfSentences[0])

    def GetReviewTestByReviewId(self, reviewId):
        listOfSentences = self.__featureProvider.GetReviewSentencesById(reviewId)
        print "GetReviewTestByReviewId"
        print len(listOfSentences)
        return self.__GetReviewObjects(reviewId,listOfSentences[0])
             
    def MergeToReview(self, listOfSentences, listOfFeaturesIds):
        reviews = []
        sentencesIdsList = [row[0] for row in listOfSentences]
        reviewIdList = list(OrderedDict.fromkeys([row[3] for row in listOfSentences]))
        
        listOfDict = []
        listOfFeaturesInSetences = {}
        for i in xrange((len(sentencesIdsList)/2000)+1):
            listOfDict.append(self.__featureProvider.GetFeatureAsIsInSentences(sentencesIdsList[i*2000:i*2000+2000], listOfFeaturesIds))
          
        listOfFeaturesInSetences =   dict((k,v) for d in listOfDict for (k,v) in d.items())
        for reviewId in reviewIdList:
            review = ''
            reviewsSentecesOrdered = sorted(list( filter((lambda s: s[3] == reviewId), listOfSentences)), key=lambda tup: tup[4])
            for sentences in reviewsSentecesOrdered:
                text = sentences[1]
                for feature in listOfFeaturesIds:
                    if (int(feature),sentences[0]) in listOfFeaturesInSetences:
                        text = text.replace(listOfFeaturesInSetences[(int(feature),sentences[0])],'<feature_in_text id="'+str(feature)+'">'+listOfFeaturesInSetences[(int(feature),sentences[0])]+'</feature_in_text>')
                review = review + '<sentences_in_text id="'+str(sentences[0])+'" polarity="'+str(sentences[2])+u'">'+text+u'</sentences_in_text>'
            reviews.append('<review id="'+str(reviewId)+'">' + review + '</review>')
        print '**' 
        return reviews

    def __GetListOfReviewsId(self, listOfSentences):
        reviewsIds = []
        for sentence in listOfSentences:
            reviewId = sentence[1]
            if reviewId not in reviewsIds:
                reviewsIds.append(reviewId) 
        return reviewsIds

    def __GetListOfReviewSentences(self, reviewId, listOfSentences):
        return sorted(list( filter((lambda s: s[1] == reviewId), reviewSentences)), key=lambda tup: tup[4])

    def __GetListOfReviewSentecesId(self,reviewId,listOfSentences):
        sentencesId = []
        for sentence in listOfSentences:
            sentenceId = sentence[0]
            if sentenceId not in sentencesId:
                sentencesId.append(sentenceId) 
        return sentencesId

    def __GetListOfSentenceFeatures(self, sentenceId, listOfSentences):     
        return dict([(sentence[5],sentence[3])  for sentence in  list( filter((lambda s: s[0] == sentenceId), listOfSentences))])

    def __GetListOfReviewFeatures(self, reviewId, listOfSentences):     
        featureDict = dict([(sentence[3],sentence[5])  for sentence in  list( filter((lambda s: s[1] == reviewId), listOfSentences))])
        if None in featureDict.keys():
            del featureDict[None]
        return featureDict

    
    def __GetSentenceObjects(self, sentenceId, listOfSentences):
       
        sentence = Sentence()
        sentenceList = list (filter((lambda s: s[0] == sentenceId), listOfSentences))
        featuresDict = self.__GetListOfSentenceFeatures( sentenceId, sentenceList)
        sentenceText = sentenceList[0][2]
        sentence.SetId(sentenceId)
        sentence.SetFeatures(featuresDict if len(featuresDict) >= 1 and None not in featuresDict.keys() else {})
        sentence.SetPolarity(sentenceList[0][7])
        if len(featuresDict) > 0 :
            for feature in featuresDict.keys():
                if feature is not None:
                    sentenceText = sentenceText.replace(feature,"@@@#@@@"+str(feature)+"@@@#@@@")
            members = sentenceText.split("@@@#@@@")   
            for member in members:
                sMember = SentenceMember()
                if member in featuresDict.keys():
                    sMember.SetText(member)
                    sMember.SetFeatureId(featuresDict[member])
                else:
                    sMember.SetText(member)
                sentence.AddMember(sMember)
        else:
            member = SentenceMember()
            member.SetText(sentenceText)
            sentence.AddMember(member)
        
        return sentence
        
    def __GetReviewObjects(self, reviewId, listOfSentences):
        review = Review()
        listOfReviewSentencesId = self.__GetListOfReviewSentecesId(reviewId, listOfSentences)
        review.SetId(reviewId)
        review.SetFeatures(self.__GetListOfReviewFeatures(reviewId, listOfSentences))
        for sentencesId in listOfReviewSentencesId:
            review.AddSentence(self.__GetSentenceObjects(sentencesId, listOfSentences))
       
        review.SetPolarity(CalculatePolarity(review.GetListOfSentencesPolarity()))
        return review
       
    def __GetItemObject(self, itemid, listOfSentences):
        item = Item()
        listOfItemsReviewsId = self.__GetListOfReviewsId( listOfSentences)
        item.SetId(itemid)
        item.SetPolarity(CalculatePolarity([sentence[7] for sentence in listOfSentences]))
       
        for reviewId in listOfItemsReviewsId:
            listOfReviewSentences = [s for s in listOfSentences if s[1] == reviewId]
            item.AddReview(self.__GetReviewObjects(reviewId, listOfReviewSentences))
        return item
