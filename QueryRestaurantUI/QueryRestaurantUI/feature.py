import sys
from QueryRestaurantUI import app
from flask import render_template
from flask import jsonify
from flask import Flask
from flask import request
from connector import getEngineUrl
from DBHelper import sourceDBProvider
import urllib2
import ast


@app.route('/allfeatures')
def GetAllFeatures():
    try:

        url = getEngineUrl() + "/querygetallfeatures"
        itemsInStrArr = urllib2.urlopen(url).read()
        items = ast.literal_eval(itemsInStrArr)
        print items
    except:
        e = sys.exc_info()[0]
        print e
    return jsonify({'features': sorted(items, key=lambda x: x[0])})

@app.route('/getitemswithfeatures', methods=['GET'])
def getItemsWithfeatures():
    try:
       items = request.args.get('items', '')
       features = request.args.get('features', '')
       args = '?items={0}&features={1}'.format(items,features)
       url = getEngineUrl()+"/querygetitemswithfeatures"+args
       itemsInStrArr = urllib2.urlopen(url).read()
       items = ast.literal_eval(itemsInStrArr)
    except:
       e = sys.exc_info()[0]
       print e
    return jsonify({'items':items})

@app.route('/getitemsidbyfeaturelist')
def GetItemsIdByFeatureList():
    try:
        featureList = request.args.get('featurelist')

        args = '?featurelist={0}'.format(featureList)
        url = getEngineUrl() + "/querygetitemsidbyfeaturelist" + args
        itemsInStrArr = urllib2.urlopen(url).read()
        items = ast.literal_eval(itemsInStrArr)
    except:
        e = sys.exc_info()[0]
        print e
    return jsonify({'items': items})


@app.route('/getfeaturesbyitemsid', methods=['GET'])
def GetFeatureByItemsId():
    try:
       itemsStr = request.args.get('items', '')
       args = '?items={0}'.format(itemsStr)
       url = getEngineUrl()+"/querygetfeaturesbyitemsid"+args
       featuresInStrArr = urllib2.urlopen(url).read()
       features = ast.literal_eval(featuresInStrArr)
    except:
       e = sys.exc_info()[0]
       print e
    return jsonify({'features':features})


@app.route('/searchitemsbyfeatures', methods=['GET'])
def SearchItemsByFeatures():
    try:
       featuresList = request.args.get('features')
       args = '?features={0}'.format(featuresList)
       url = getEngineUrl()+"/querysearchitemsbyfeatures"+args
       dataItemAndFeatures = urllib2.urlopen(url).read()
       info = ast.literal_eval(dataItemAndFeatures)
    except:
       e = sys.exc_info()[0]
       print e
    return jsonify(info)

@app.route('/getfeatureinfo', methods=['GET'])
def GetFeatureInfo():
    try:
       featuresList = request.args.get('featureId')
       args = '?featureId={0}'.format(featuresList)
       url = getEngineUrl()+"/querygetfeatureinfo"+args
       feautreInfo = urllib2.urlopen(url).read()
       info = ast.literal_eval(feautreInfo)
       items = info["items"]
       print items
       itemsinfo = {}
       for item in items:
           data = sourceDBProvider.GetRestaurantInfo([item])
           if len(data) > 0 and len(data[0]) > 0 :
               itemsinfo[item] = data[0][0]
       info["items"] = itemsinfo
    except:
       print 'error in getfeatureinfo'
       e = (sys.exc_info)[0]
       print e
    return jsonify(info)
