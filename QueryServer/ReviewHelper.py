from SentimentPolarity import CalculatePolarity
from CommonTypes import Polarity
from collections import OrderedDict
from QObjects import SentenceMember, Sentence, Review, Item


class ReviewHelper(object):
    __featureProvider = None
    def __init__(self, featureProvider):
        self.__featureProvider = featureProvider
            
       
    def GetReviewsSentencesByFeatureIds(self, featureidsList):
        
        print self.__featureProvider.GetReviewsSentencesByFeatureIds(featureidsList)[0]

    def GetReviewsTextByItemIdAndFeatureIds(self,itemId, featureIdsList, polarity = Polarity.ALL):
        #1.get all reviews sentences
        listOfSentences = self.__featureProvider.GetReviewsSentencesByItemsAndFeatureIds(itemId,featureIdsList)
        #2.get review sentences and mark features if exists
        #3.marge review's senteces to one text block
        return self.MergeToReview(listOfSentences[0], featureIdsList)
        
    def GetReviewsTextByFeatureIds(self, featureIdsList, polarity = Polarity.ALL):
        listOfSentences = self.__featureProvider.GetReviewsSentencesByFeatureIds(featureIdsList)
        return self.MergeToReview(listOfSentences[0], featureIdsList)

    def GetReviewsTextByItemId(self, itemId):
        listOfSentences = self.__featureProvider.GetReviewsSentencesByFeatureIds(itemId)
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
        print listOfFeaturesInSetences
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

    def __GetSentenceObjects(self, sentenceId, listOfSentences):
        sentence = Sentence()
        sentenceList = list (filter((lambda s: s[0] == sentenceId), listOfSentences))
        featuresDict = self.__GetListOfSentenceFeatures( sentenceId, sentenceList)
        sentenceText = sentenceList[0][2]
        sentence.id = sentenceId
        sentence.polarity = sentenceList[0][7]
        if len(featuresDict) > 0 :
            for feature in featuresDict.keys():
                if feature is not None:
                    sentenceText = sentenceText.replace(feature,"@@@#@@@"+str(feature)+"@@@#@@@")
            members = sentenceText.split("@@@#@@@")   
            for member in members:
                sMember = SentenceMember()
                if member in featuresDict.keys():
                    sMember.text = member
                    sMember.id = featuresDict[member]
                else:
                    sMember.text = member
                sentence.AddMember(sMember)
        else:
            member = SentenceMember()
            member.text = sentenceText
            sentence.AddMember(member)
        
        return sentence
        
    def __GetReviewObjects(self, reviewId, listOfSentences):
        review = Review()
        listOfReviewSentencesId = self.__GetListOfReviewSentecesId(reviewId, listOfSentences)
        review.id = reviewId
        for sentencesId in listOfReviewSentencesId:
            review.AddSentence(self.__GetSentenceObjects(sentencesId, listOfSentences))
        print review.sentences    
        review.polarity = CalculatePolarity([sentence.polarity for sentence in review.sentences])
        return review
       
    def __GetItemObject(self, itemid, listOfSentences):
        item = Item()
        listOfItemsReviewsId = self.__GetListOfReviewsId( listOfSentences)
        item.id = itemid
        for reviewId in listOfItemsReviewsId:
            item.AddReview(self.__GetReviewObjects(reviewId, listOfSentences))  
            
        item.polarity = CalculatePolarity([sentence[7] for sentence in listOfSentences])
        return item
