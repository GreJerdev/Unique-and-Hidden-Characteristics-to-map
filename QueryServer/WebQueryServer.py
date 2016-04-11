from flask import Flask
from flask import request
from configurationLoader import GetConfiguraton

from QueryServer import QueryServer
app = Flask(__name__)
query = None

@app.route("/getfeatures",methods=['GET'])
def GetFeatures():
    p = type('point', (object,), {}) 
    p.dis = 2

    lat = request.args.get('lat', '')
    lon = request.args.get('lon', '')
    try:
        float(lat)
        float(lon)
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
        return '[]'
    p.lat = lat
    p.lon = lon
    responce = str(query.GetItems(p))
    return  responce


@app.route("/getfeaturebyitemid",methods=["GET"])
def GetFeatureByItemId():
    itemId = request.args.get('itemId', '')
    try:
        print itemId
        responce = str(query.GetFeatureByItemId(itemId))
        print responce
    except:
        pass
        #print  sys.exc_info()
        #print "END OF ERROR"
    return responce


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
        
if __name__ == "__main__":
    configXml = GetConfiguraton(None)
    query  = QueryServer(configXml)
    app.run()
