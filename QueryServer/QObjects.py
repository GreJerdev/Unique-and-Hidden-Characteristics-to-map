
def GetEmptyObject(name):
    return type(str(name), (object,), {}) 


def Item_to_dict(row):
    d = dict()
    d['Name'] = row[0]
    d['id'] = row[1]
    d['lat'] = row[2]
    d['lng'] = row[3]
    d['distance'] = row[4]
    return d

class SentenceMember(dict):


    def SetText(self,text):
        self['text'] = text
        
    def SetFeatureId(self,text):
        self['featureId'] = text

    def GetText(self):
        return self['text'] 
        
    def GetFeatureId(self):
        return self['featureId'] 

        
    

class Sentence(dict):   

    def __init__(self):
        self.SetPolarity(0)
        self.SetId(0)
        self['members'] = [] 

    def SetPolarity(self,text):
        self['polarity'] = text

    def SetId(self,text):
        self['id'] = text

    def GetPolarity(self):
        return self['polarity'] 
        
    def GetId(self):
        return self['id']

    def GetMembers(self):
        return self['members'] 

    def AddMember(self, member):
        self['members'].append(member)
        
   
class Review(dict):

    def __init__(self):
        self.SetPolarity(0)
        self.SetId(0)
        self['sentences'] = [] 

    def SetPolarity(self, polarity):
        self['polarity'] = polarity

    def SetId(self,text):
        self['id'] = text

    def GetPolarity(self):
        return self['polarity'] 
        
    def GetId(self):
        return self['id']

    def GetSentence(self):
        return self['sentences']

    
    def AddSentence(self, sentence):
        self['sentences'].append(sentence)

    def GetListOfSentencesPolarity(self):
        return  [sentence['polarity'] for sentence in self.GetSentence() if 'polarity' in sentence.keys()]
        
                                                                        

class Item(dict):

    def __init__(self,temperature = 0):
        self._temperature = temperature
        self.SetPolarity(0)
        self.SetId(0)
        self['reviews'] = [] 

    def SetPolarity(self, polarity):
        self['polarity'] = polarity

    def SetId(self,text):
        self['id'] = text

    def GetPolarity(self):
        return self['polarity'] 

    def GetId(self):
        return self['id']

    def GetReview(self):
        return self['reviews']
    
    def AddReview(self, sentence):
        self['reviews'].append(sentence)

