from QueryRestaurantUI import app
from flask import render_template
from flask import jsonify
from flask import Flask
from flask import request
from connector import getEngineUrl
import urllib2
import ast

print getEngineUrl()
             
@app.route('/getitemswithfeatures', methods=['GET', 'POST'])
def getItemsWithfeatures():
    try:
       items = request.args.get('items', '')
       features = request.args.get('features', '')
       args = '?items={0}&features={1}'.format(items,features)
       url = getEngineUrl()+"/getitemswithfeatures"+args
       itemsInStrArr = urllib2.urlopen(url).read()
       items = ast.literal_eval(itemsInStrArr)
    except:
       e = sys.exc_info()[0]
       print e  
    return jsonify({'items':items})

@app.route('/getitemsnearme', methods=['GET', 'POST'])
def getItemsNearMe():
    try:
       lat = request.args.get('lat', '')
       lon = request.args.get('lon', '')
       print lat
       print lon
       args = '?lat={0}&lon={1}'.format(lat,lon)
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
       #print lat
       #print lon
       args = '?lat={0}&lon={1}'.format(lat,lon)
       url = getEngineUrl()+"/getfeatures"+args
       print url 
       featuresInStrArr = urllib2.urlopen(url).read()
       features = ast.literal_eval(featuresInStrArr)
    except:
       e = sys.exc_info()[0]
       print e  
    return jsonify({'features':features})
