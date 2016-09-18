from QueryRestaurantUI import app
from flask import render_template
from flask import jsonify
from flask import Flask
from flask import request
import urllib2
import ast

serverUrl = 'dilixo.net'
postfix = 'UniqueHiddenCharacteristics'
port = '80'
protocol = 'http'

def getEngineUrl():
    return '{0}://{1}:{2}/{3}'.format(protocol,serverUrl,port,postfix)
