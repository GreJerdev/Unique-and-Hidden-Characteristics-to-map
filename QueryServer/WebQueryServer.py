import sys
from flask import Flask
from flask import request
from flask import jsonify
from configurationLoader import GetConfiguraton

from QueryServer import QueryServer
import tools

app = Flask(__name__)
query = None


@app.route("/querygetallfeatures",methods=['GET'])
def GetAllFeatures():
    responce = str(query.GetAllFeatures())
    return  responce

@app.route("/querygetallitems",methods=['GET'])
def GetAllItems():
    items = query.GetAllItems()
    responce = jsonify({'items':items})
    return  responce

@app.route("/querygetfeatures",methods=['GET'])
def GetFeatures():
    p = type('point', (object,), {}) 
    p.dis = 2

    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    distance = request.args.get('distance', '2')
    try:
        float(lat)
        float(lon)
        float(distance)
    except ValueError:
        return '[]'
    p.lat = lat
    p.lon = lon
    p.dis = distance
    responce = str(query.GetFeature(p))
    return  responce

@app.route("/querygetfeatureinfo",methods=['GET'])
def GetFeatureInfo():
    featureId = request.args.get('featureId', '')
    responce = str(query.GetFeatureInfo(featureId))
    return  responce


@app.route("/querygetfeaturesbyitemsid",methods=['GET'])
def GetFeatureByItemsId():
    itemsStr = request.args.get('items', '')
    itemsArr = itemsStr.split(',')    
        
    features = query.GetFeatureByItemsId(itemsArr)
    responce = str(features)
    return  responce

    
@app.route("/querygetitems",methods=['GET'])
def GetItems():
    p = type('point', (object,), {}) 
    p.dis = 2

    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    distance = request.args.get('distance', '')
    try:
        float(lat)
        float(lon)
        float(distance)
    except ValueError:
        print 'error'
        return '[]'
        
    p.lat = lat
    p.lon = lon
    p.dis = distance
    items = query.GetItems(p)
    responce = jsonify({'items':items})
    return  responce


@app.route("/querygetfeaturebyitemid",methods=["GET"])
def GetFeatureByItemId():
    itemId = request.args.get('id', '')
    try:
        responce = query.GetFeatureByItemId(itemId)
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return str(responce)


@app.route("/querygetsimilaritems",methods=['GET'])
def GetSimilarItems():
    itemid = request.args.get('id', '')
    try:
        itemid_int = int(itemid)
        responce = str(query.GetSimilarItems(itemid_int))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/querygetitemsidbyfeaturelist",methods=['GET'])
def GetItemsIdByFeatureList( ):
    featureList = request.args.get('featurelist', '')
    try:
        featureIdArr = featureList.split(',')
        print featureIdArr
        responce = str(query.GetItemsIdByFeatureList(featureIdArr))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/querycomperbetweenitems",methods=['GET'])
def ComperBetweenItems():
    itemsIdList = request.args.get('itemsIdList', '')
    try:
        responce = str(query.ComperBetweenItems(itemsIdList.split(',')))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/querygetitemreviewsidbyitemid",methods=['GET'])
def GetItemReviewsIdByItemId():
    itemid = request.args.get('itemId', '')
    try:
        responce = str(query.GetItemReviewsIdByItemId(itemid))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/querygetfeaturepolarityinitemreviews",methods=['GET'])
def GetFeaturePolarityInItemReviews():
    featureId = request.args.get('featureId', '')
    itemId = request.args.get('itemId', '')
    print featureId,itemId
    try:
        responce = query.GetFeaturePolarityInItemReviews(featureId,itemId)
    except:
        print "Begin OF ERROR"
        print  sys.exc_info()
        print "END OF ERROR"
    return str(responce)

@app.route("/querygetfeaturepolarityinreviews",methods=['GET'])
def GetFeaturePolarityInReviews():
    featureId = request.args.get('featureId', '')
    reviewId = request.args.get('reviewId', '')
    try:
        itemid_int = int(itemid)
        responce = str(query.GetFeaturePolarityInReviews(featureId,reviewId))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/querygetfeaturepolarityglobal",methods=['GET'])
def GetFeaturePolarityGlobal():
    featureId = request.args.get('featureId', '')
    try:
       
        responce = str(query.GetFeaturePolarityGlobal(featureId))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/querygetreviewstextbyitemIdandfeatureIds",methods=['GET'])
def GetReviewsTextByItemIdAndFeatureIds(itemId, featureIdsList):
    itemid = request.args.get('itemId', '')
    featureIdsList = request.args.get('featureIdsList', '')
    try:
        itemid_int = int(itemid)
        responce = str(query.GetReviewsTextByItemIdAndFeatureIds(itemId, featureIdsList))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/querygetreviewstextbyfeatureIds",methods=['GET'])
def GetReviewsTextByFeatureIds():
    featureIds = request.args.get('featureIdsList', '')
    featureIdsList = featureIds.split(',')
    
    print featureIdsList
    print '-----------------'
    try:
        responce = str(query.GetReviewsTextByFeatureIds(featureIdsList))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route('/querygetitemswithfeatures', methods=['GET', 'POST'])
def getItemsWithFeatures():
    try:     
        itemsStr = request.args.get('items', '')
        featuresStr = request.args.get('features', '')
        items = itemsStr.split(',')
        features = featuresStr.strip(',').split(',')
        items = [i for i in items if len(i) > 0  ]
        features = [f for f in features if len(f) > 0  ]
        result = query.GetItemsWithFeatures(items,features)
        responce = str(result)
    except:
        e = sys.exc_info()[0]
        print e  
    return responce

@app.route('/querygetreviewsentencesbyid', methods=['GET', 'POST'])
def GetReviewSentencesById():
    id = request.args.get('id', '')
    result = {}
    if tools.IsInt(id):
        result = query.GetItemsWithFeatures(id)
    return str(result)

@app.route('/querygetreviewsentencesbyitemid', methods=['GET', 'POST'])
def GetReviewsTextByItemId():
    id = request.args.get('id', '')
    result = {}
    print id
    if tools.IsInt(id):
        result = query.GetReviewsTextByItemId(id)
    return str(result)

@app.route('/querysearchitemsbyfeatures', methods=['GET'])
def SearchItemsByFeatures():
    featuresStr = request.args.get('features', '')
    features = featuresStr.strip(',').split(',')
    result = query.SearchItemsByFeatures(features)
    return str(result)


@app.route('/querygetitemfeaturesandfeaturesentencesbyitemid')
def GetItemFeaturesAndFeatureSentencesByItemId():
    responce = {}    
    try: 
        featuresStr = request.args.get('id', '')
        id = request.args.get('id', '')
        if tools.IsInt(id):
            result = query.GetItemFeaturesAndFeatureSentencesByItemId(id)
            responce = jsonify(result)
       
    except:
            e = sys.exc_info()[0]
            print e  
    return responce
    

if __name__ == "__main__":
    configXml = GetConfiguraton(None)
    query  = QueryServer(configXml)
    app.run()
