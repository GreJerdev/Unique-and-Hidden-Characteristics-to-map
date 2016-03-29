from SentimentPolarity import CalculatePolarity
from CommonTypes import Polarity
from collections import OrderedDict

class Review(object):
    __sentences = []
    __features = []
    __polarity = 0



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
