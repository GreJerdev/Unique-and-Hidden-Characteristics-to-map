from flask import Flask
from flask import request
from flask import jsonify
from configurationLoader import GetConfiguraton

from QueryServer import QueryServer
import tools

app = Flask(__name__)
query = None


@app.route("/getallfeatures",methods=['GET'])
def GetAllFeatures():
    responce = str(query.GetAllFeatures())
    return  responce

@app.route("/getallitems",methods=['GET'])
def GetAllItems():
    items = query.GetAllItems()
    responce = jsonify({'items':items})
    return  responce

@app.route("/getfeatures",methods=['GET'])
def GetFeatures():
    p = type('point', (object,), {}) 
    p.dis = 2

    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    try:
        float(lat)
        float(lon)
        print "hellow Irina"
    except ValueError:
        return '[]'
    p.lat = lat
    p.lon = lon
    responce = str(query.GetFeature(p))
    return  responce

@app.route("/getitems",methods=['GET'])
def GetItems():
    p = type('point', (object,), {}) 
    p.dis = 2

    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    try:
        float(lat)
        float(lon)
    except ValueError:
        print 'error'
        return '[]'
        
    p.lat = lat
    p.lon = lon
    items = query.GetItems(p)
    responce = jsonify({'items':items})
    return  responce


@app.route("/getfeaturebyitemid",methods=["GET"])
def GetFeatureByItemId():
    itemId = request.args.get('itemId', '')
    try:
        responce = query.GetFeatureByItemId(itemId)
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return jsonify({'features':responce})


@app.route("/getsimilaritems",methods=['GET'])
def GetSimilarItems():
    itemid = request.args.get('item', '')
    try:
        itemid_int = int(itemid)
        responce = str(query.GetSimilarItems(itemid_int))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/getitemsidbyfeaturelist",methods=['GET'])
def GetItemsIdByFeatureList( ):
    featureList = request.args.get('featurelist', '')
    try:
        itemid_int = int(itemid)
        responce = str(query.GetItemsIdByFeatureList(featureList))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/comperbetweenitems",methods=['GET'])
def ComperBetweenItems():
    itemsIdList = request.args.get('itemsIdList', '')
    try:
        responce = str(query.ComperBetweenItems(itemsIdList.split(',')))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/getitemreviewsidbyitemid",methods=['GET'])
def GetItemReviewsIdByItemId():
    itemid = request.args.get('itemId', '')
    try:
        responce = str(query.GetItemReviewsIdByItemId(itemid))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/getfeaturepolarityinitemreviews",methods=['GET'])
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

@app.route("/getfeaturepolarityinreviews",methods=['GET'])
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

@app.route("/getfeaturepolarityglobal",methods=['GET'])
def GetFeaturePolarityGlobal():
    featureId = request.args.get('featureId', '')
    try:
       
        responce = str(query.GetFeaturePolarityGlobal(featureId))
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return  responce

@app.route("/getreviewstextbyitemIdandfeatureIds",methods=['GET'])
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

@app.route("/getreviewstextbyfeatureIds",methods=['GET'])
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

@app.route('/getitemswithfeatures', methods=['GET', 'POST'])
def getItemsWithFeatures():
    try:     
        itemsStr = request.args.get('items', '')
        featuresStr = request.args.get('features', '')
        items = itemsStr.split(',')
        features = featuresStr.strip(',').split(',')
        items = [i for i in items if len(i) > 0  ]
        features = [f for f in features if len(f) > 0  ]
        print '--features--'
        print features
        print '--items--'
        print items
        result = query.GetItemsWithFeatures(items,features)
        print 'result'
        print result
        responce = str(result)
    except:
        e = sys.exc_info()[0]
        print e  
    return responce

@app.route('/getreviewsentencesbyid', methods=['GET', 'POST'])
def GetReviewSentencesById():
    id = request.args.get('id', '')
    result = {}
    if tools.IsInt(id):
        result = query.GetItemsWithFeatures(id)
    return str(result)

@app.route('/getreviewsentencesbyitemid', methods=['GET', 'POST'])
def GetReviewsTextByItemId():
    id = request.args.get('id', '')
    result = {}
    print id
    if tools.IsInt(id):
        result = query.GetReviewsTextByItemId(id)
    return str(result)
        
if __name__ == "__main__":
    configXml = GetConfiguraton(None)
    query  = QueryServer(configXml)
    app.run()
