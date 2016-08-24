from QueryRestaurantUI import app
from flask import render_template
from flask import jsonify
from flask import Flask
from flask import request
from connector import getEngineUrl
import urllib2
import ast

print getEngineUrl()
             


@app.route('/getitemsnearme', methods=['GET', 'POST'])
def getItemsNearMe():
    try:
       lat = request.args.get('lat', '')
       lon = request.args.get('lon', '')
       distance = request.args.get('distance', '')
       args = '?lat={0}&lon={1}&distance={2}'.format(lat,lon,distance)
       url = getEngineUrl()+"/getitems"+args
       itemsInStrArr = urllib2.urlopen(url).read()
       items = ast.literal_eval(itemsInStrArr)
    except:
       e = sys.exc_info()[0]
       print e  
    return jsonify({'items':items})


@app.route('/getfeaturesnearme', methods=['GET', 'POST'])
def getFeatureNearMe():
    try:
       lat = request.args.get('lat', '')
       lon = request.args.get('lon', '')
       distance = request.args.get('distance', '')
       args = '?lat={0}&lon={1}&distance={2}'.format(lat,lon,distance)
       url = getEngineUrl()+"/getfeatures"+args
       featuresInStrArr = urllib2.urlopen(url).read()
       features = ast.literal_eval(featuresInStrArr)
    except:
       e = sys.exc_info()[0]
       print e  
    return jsonify({'features':features})
