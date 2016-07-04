from QueryRestaurantUI import app
from flask import render_template
from flask import jsonify
from flask import Flask
from flask import request
import urllib2
import ast

serverUrl = '127.0.0.1'  
port = '5000'
protocol = 'http'

def getEngineUrl():
    return '{0}://{1}:{2}'.format(protocol,serverUrl,port)
