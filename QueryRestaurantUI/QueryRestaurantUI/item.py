import sys
import urllib2
import ast

from flask import render_template
from flask import jsonify
from flask import Flask
from flask import request
from QueryRestaurantUI import app
from connector import getEngineUrl
from DBHelper import sourceDBProvider

import time

@app.route('/allpoints')
def GetAllItems():
    try:
        url = getEngineUrl() + "/querygetallitems"

        itemsInStrArr = urllib2.urlopen(url).read()
        items = ast.literal_eval(itemsInStrArr)
    except:
        e = sys.exc_info()[0]
        print e
    return jsonify({'items': items})

@app.route('/getreviewsentencesbyid', methods=['GET', 'POST'])
def GetReviewSentencesById():
    try:
       id = request.args.get('id', '')
       args = '?id={0}'.format(id)
       url = getEngineUrl()+"/querygetreviewsentencesbyid"+args
       itemsInStrArr = urllib2.urlopen(url).read()
       items = ast.literal_eval(itemsInStrArr)
    except:
       e = sys.exc_info()[0]
       print e  
    return jsonify(items)

@app.route('/getreviewsentencesbyitemid', methods=['GET', 'POST'])
def GetReviewsTextByItemId():
    try:
        
        id = request.args.get('id', '')
        args = '?id={0}'.format(id)
        url = getEngineUrl()+"/querygetreviewsentencesbyitemid"+args
        print url
        itemsInStrArr = urllib2.urlopen(url).read()
        print len(itemsInStrArr)
        items = ast.literal_eval(itemsInStrArr)
    except:
        e = sys.exc_info()[0]
        print e  
    return jsonify(items)

@app.route('/getitem',methods=['GET', 'POST'])
def GetItem():
    result = {}
    start_time = time.time()

    try:
        id = request.args.get('id', '')
        args = '?id={0}'.format(id)
        url = getEngineUrl() + "/querygetitemfeaturesandfeaturesentencesbyitemid" + args
        print url
        featuresInfo = {}
        featuresInfo = ast.literal_eval(urllib2.urlopen(url).read())
        print("---getitemfeaturesandfeaturesentencesbyitemid %s seconds ---" % (time.time() - start_time))
        item = sourceDBProvider.GetRestaurantInfo([id])
        print("---GetRestaurantInfo %s seconds ---" % (time.time() - start_time))
        result['restaurantInfo'] = {}
        result['restaurantInfo']['id'] = item[0][0][0]
        result['restaurantInfo']['city'] = item[0][0][1]
        result['restaurantInfo']['name'] = item[0][0][2]
        result['restaurantInfo']['type'] = item[0][0][3]
        result['restaurantInfo']['full_address'] = item[0][0][4]
        result['restaurantInfo']['hours'] = ast.literal_eval(item[0][0][5])
        result['restaurantInfo']['stars'] = item[0][0][6]
        result['restaurantInfo']['attributes'] = ast.literal_eval(item[0][0][7])
        result['restaurantInfo']['categories'] = ast.literal_eval(item[0][0][8])
        print result['restaurantInfo']
        result['restaurantInfo']['photos'] = []
        if(len(item) > 1):
            result['restaurantInfo']['photos'] = [str( photo[3] )+'.jpg' for photo in item[1]]
        result['featuresInfo'] = featuresInfo
    except:
        e = sys.exc_info()[0]
        print e
    return jsonify(result)



"""
@app.route('/getitem',methods=['GET', 'POST'])
def GetItem():
    result = {'reviews':{},'features':{},'similarItems':{}}
    try:
        id = request.args.get('id', '')
        args = '?id={0}'.format(id)
        url = getEngineUrl() + "/getreviewsentencesbyitemid" + args
        itemsInStrArr = urllib2.urlopen(url).read()
        items = {}
        items = ast.literal_eval(itemsInStrArr)
        url = getEngineUrl() + "/getfeaturebyitemid" + args
        features = {}
        features = ast.literal_eval(urllib2.urlopen(url).read())
        url = getEngineUrl() + "/getsimilaritems" + args
        similaritems = {}
        #similaritems  = ast.literal_eval(urllib2.urlopen(url).read())
        result['restaurantInfo'] =  {item[0][0]: list(item[0]) for item in  sourceDBProvider.GetRestaurantInfo([id])}
        result['reviews'] = items['reviews']
        result['features'] = features
        result['similarItems'] = similaritems
    except:
        e = sys.exc_info()[0]
        print e
    return jsonify(result)
"""
