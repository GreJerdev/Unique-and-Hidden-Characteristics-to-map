from QueryRestaurantUI import app
from flask import render_template
from flask import jsonify
from flask import Flask
from flask import request
from connector import getEngineUrl
import urllib2
import ast
import locations
import item
import feature

@app.route('/')
def index():
    return render_template('main.html')



    


