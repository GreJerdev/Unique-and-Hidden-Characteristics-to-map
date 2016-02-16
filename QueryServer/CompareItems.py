from math import sqrt

def CreateAllFeaturesDicEmptyDic(itemsAndFeatures):
    featureDic = {}
    for item in itemsAndFeatures.keys():
        for featureId in itemsAndFeatures[item].keys():
            featureDic[featureId]= 0

    return featureDic


def CreateCompareTableBetweenItems(itemsAndFeatures):
    compareItemsDic = {}
    emptyAllfeaturesDic = CreateAllFeaturesDicEmptyDic(itemsAndFeatures)
    for item in itemsAndFeatures.keys():
        compareItemsDic[item] = emptyAllfeaturesDic.copy()
        for featureId in itemsAndFeatures[item].keys():
             compareItemsDic[item][featureId] = itemsAndFeatures[item][featureId]
    return compareItemsDic




def CalculateDistance (dictFeatureA,dictFeatureB):
        return sqrt(sum([(dictFeatureA[feature]-dictFeatureB[feature])**2 for feature in dictFeatureA.keys()]))
    
