from math import sqrt

def CreateAllFeaturesDicEmptyDic(itemsAndFeatures):
    featureDic = {}
   
    for item in itemsAndFeatures.keys():
        for featureId in itemsAndFeatures[item].keys():
            featureDic[featureId] = {'tf_idf':0,'text':itemsAndFeatures[item][featureId]['text'],'polarity':0}
            
    return featureDic


def CreateCompareTableBetweenItems(itemsAndFeatures):
    compareItemsDic = {}
    print 1 
    emptyAllfeaturesDic = CreateAllFeaturesDicEmptyDic(itemsAndFeatures)
    
    for item in itemsAndFeatures.keys():
        compareItemsDic[item] = emptyAllfeaturesDic.copy()
        for featureId in itemsAndFeatures[item].keys():
           
            compareItemsDic[item][featureId] = itemsAndFeatures[item][featureId]
    return compareItemsDic




def CalculateDistance (dictFeatureA,dictFeatureB):
        return sqrt(sum([(dictFeatureA[feature]['tf_idf']-dictFeatureB[feature]['tf_idf'])**2 for feature in dictFeatureA.keys()]))
    
