from QueryRestaurantUI import app
from flask import render_template
from flask import jsonify
from flask import Flask
from flask import request
from connector import getEngineUrl
import urllib2
import ast
import locations

@app.route('/')
def index():
    return render_template('main.html')


@app.route('/allpoints')
def GetAllItems():
    try:
       url = getEngineUrl()+"/getallitems"
       
       itemsInStrArr = urllib2.urlopen(url).read()
       items = ast.literal_eval(itemsInStrArr)
    except:
       e = sys.exc_info()[0]
       print e
    return jsonify({'items':items})
    
 
@app.route('/allfeatures')
def GetAllFeatures():
    try:
     
       url = getEngineUrl()+"/getallfeatures"
       itemsInStrArr = urllib2.urlopen(url).read()
       items = ast.literal_eval(itemsInStrArr)
    except:
       e = sys.exc_info()[0]
       print e  
    return jsonify({'features':items})

