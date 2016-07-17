
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

class SentenceMember(object):
    text = ""
    featureId = ""
    def __str__(self):
        return str(self.__dict__)



class Sentence(object):

    polarity = 0
    id = 0
    members = []

    def AddMember(self, member):
        self.members.append(member)
        
    def __str__(self):
        return str(self.__dict__)+ str(self.members)

class Review(object):

    polarity = 0
    id = 0
    sentences = []

    def AddSentence(self, sentence):
        self.sentences.append(sentence)

    def __str__(self):
        return str(self.__dict__) + str(self.sentences)

class Item(object):

    polarity = 0
    id = 0
    reviews = []

    def AddReview(self, review):
        self.reviews.append(review)

    def __str__(self):
        return str(self.__dict__)
