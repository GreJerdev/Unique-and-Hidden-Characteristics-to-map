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

@app.route('/allpoints')
def GetAllItems():
    try:
        url = getEngineUrl() + "/getallitems"

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
       url = getEngineUrl()+"/getreviewsentencesbyid"+args
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
        url = getEngineUrl()+"/getreviewsentencesbyitemid"+args
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
        result['reviews'] = items['reviews']
        result['features'] = features
        result['similarItems'] = similaritems
    except:
        e = sys.exc_info()[0]
        print e
    return jsonify(result)
