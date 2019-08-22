#!/usr/bin/env python

import sys, os
import random
import json
from flask import Flask, request

#insert file into path for code capture
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, root_dir)
import backtracepython as bt

from libs import appLib as al

envVarsList = ["APPLICATION_VERSION", "APPLICATION_NAME"]
globalAttributes = {}
def populateGlobalAttributes():
    for i in envVarsList:
        if i in os.environ:
            globalAttributes[i] = os.environ[i]

def createApp():
    app = Flask(__name__)
    def run_on_start(*args, **argv):
        populateGlobalAttributes()
        bt.initialize(
                endpoint=os.environ['BACKTRACE_ENDPOINT'],
                token=os.environ['BACKTRACE_TOKEN'],
                attributes=globalAttributes,
                context_line_count=3
        )
        print "bt_initialized"
    run_on_start()
    return app
app = createApp()

@app.errorhandler(Exception)
def handle_error(e):
    report = bt.BacktraceReport()
    report.capture_last_exception()
    report.send()
    return json.dumps(globalAttributes)

def authenticateUser(username, saltpw):
    return al.checkPassword(username, saltpw)

@app.route('/login', methods=['GET','POST'])
def loginHandler():
    token = -1
    errorResponse = ("{ \"msg\": \"Auth Failure\" }", 400)
    
    if request.method == "GET":
        f = open("index.html", "r")
        return f.read()

    try: 
        payload = json.loads(request.data)
    except Exception as e:
        al.sendErrror(e)
        return errorResponse
    
    if authenticateUser(payload['username'], payload['password']) is False:
        return errorResponse

    token = al.generateSession(payload['username'])
    al.log(al.LOG_INFO, "username {} authenticated. {}".format(payload['username'], token))
    return token, 200
    
if __name__== '__main__':
    app.run(host='0.0.0.0', port=80)
