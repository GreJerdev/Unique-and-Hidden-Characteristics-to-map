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
from DBHelper import susDBProvider

@app.route('/')
def index():
    print 'index'
    return render_template('main.html')


@app.route('/SusData', methods=['GET', 'POST'])
def SusData():
    print 'SusData'
    data = []
    sum = 0
    data = ''
    for x in range(1,11):
        try:
            var = int(request.args.get('q{0}'.format(x),'3'))
            data += 'q{0}={1}&'.format(x,var)
            if x%2 == 0:
                sum += 5 - var
            else:
                sum += var - 1
            data.append(var)
        except:
            pass

    score = sum * 2.5
    print score ,sum
    print dir(susDBProvider)
    susDBProvider.SaveSUSResults(request.remote_addr,data,score)
    print request.remote_addr
    return 'Thank you for help. !';




    


