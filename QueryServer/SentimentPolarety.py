from collections import defaultdict

VERY_POSITIVE = 2
POSITIVE = 1
NEUTRAL = 0
NEGATIVE = -1
VERY_NEGATIVE = -2

ERROR_PERCENT = 5

def CalculatePolaraty(polarityList):
    polarity = IsNegativePositiveOrNeutral(polarityList);
    if polarity == POSITIVE:
        polarity = IsVeryPositiveOrPositive(polarityList)
    elif polarity == NEGATIVE:
        polarity = IsVeryNegativeOrNegative(polarityList)
    return polarity    
   

def IsNegativePositiveOrNeutral(polarityList):
    polarity = NEUTRAL
    deltaErrorValue = GetDeltaErrorValue(polarityList)
    listSum = sum(polarityList)
    if (abs(listSum) - deltaErrorValue) < 0 or listSum == 0:
        polarity = NEUTRAL
    elif listSum > 0:
        polarity = POSITIVE
    elif listSum < 0:   
        polarity = NEGATIVE
    return polarity

def IsVeryPositiveOrPositive(polarityList):
    result = POSITIVE
    numberOfPositves = len([polarity for polarity in polarityList if polarity == POSITIVE])
    numberOfVeryPositves = len([polarity for polarity in polarityList if polarity == VERY_POSITIVE])
    if numberOfPositves >= numberOfVeryPositves:
        result = POSITIVE
    else:
        result = VERY_POSITIVE
    return result

def IsVeryNegativeOrNegative(polarityList):
    return (-1) * IsVeryPositiveOrPositive([polarity * (-1) for polarity in polarityList])

def GetDeltaErrorValue(polarityList):
    return (len(polarityList)/100) * ERROR_PERCENT 




print CalculatePolaraty(list([1,2,-2,-2,-1,-1,1,1,1,1,1]))
