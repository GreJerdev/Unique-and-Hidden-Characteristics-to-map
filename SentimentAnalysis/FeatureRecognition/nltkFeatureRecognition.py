from BaseFeatureRecognition import BaseFeatureRecognition
from nltk.stem import *
stemmer = PorterStemmer()

class nltkFeatureRecognition(BaseFeatureRecognition):
    
    def __init__(self):
        pass
        
    def GetFeatures(self, sentence,featureList):
        value = [stemmer.stem(plural) for plural in sentence.replace('.',' ').replace(',',' ').split()]
        return [ t for t in set(value)&set(featureList)]
