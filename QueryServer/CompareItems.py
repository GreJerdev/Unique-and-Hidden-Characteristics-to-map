

def CreateAllFeaturesDicEmptyDic(itemsAndFeatures):
    featureDic = {}
    for item in itemsAndFeatures.keys():
        for featureId in itemsAndFeatures[item].keys():
            featureDic[featureId]= 0

    return featureDic


def CreateCompareTableBetweenItems(itemsAndFeatures):
    compareItemsDic = {}
    for item in itemsAndFeatures.keys():
        compareItemsDic[item] = CreateAllFeaturesDicEmptyDic(itemsAndFeatures)
        for featureId in itemsAndFeatures[item].keys():
             compareItemsDic[item][featureId] = itemsAndFeatures[item][featureId]
    return compareItemsDic




