#!/usr/bin/env python

import sys, os
import random
import json
from flask import Flask, request, send_from_directory

#insert file into path for code capture
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, root_dir)
import backtracepython as bt

#local
from libs import appLib as al

envVarsList = ["APPLICATION_VERSION", "APPLICATION_NAME"]
globalAttributes = {}
def populateGlobalAttributes():
    for i in envVarsList:
        if i in os.environ:
            globalAttributes[i] = os.environ[i]

runtimeAttributes = {}
def appendDictasBacktraceAttributes(obj):
    pw = obj.pop('saltpw', None)
    runtimeAttributes.update(obj)
    if pw is not None:
        obj['saltpw'] = pw
    return

def appendObjBacktraceAttibutes(key, value):
    runtimeAttributes.update({ key: value })
    return

def createApp():
    app = Flask(__name__)
    def run_on_start(*args, **argv):
        populateGlobalAttributes()
        bt.initialize(
                endpoint=os.environ['BACKTRACE_ENDPOINT'],
                token=os.environ['BACKTRACE_TOKEN'],
                attributes=globalAttributes,
                context_line_count=10
        )
    run_on_start()
    return app

app = createApp()

##
# Backtrace by default provides a global exception handler that will do the equivalent of what is seen.
# Flask overrides this but provides the ability to watch for exceptions via errorhandler decorator 
##
@app.errorhandler(Exception)
def handleError(e):
    report = bt.BacktraceReport()
    report.capture_last_exception()
    report.set_dict_attributes(runtimeAttributes)
    report.send()
    return json.dumps(globalAttributes)

def authenticateUser(username, saltpw):
    return al.checkPassword(username, saltpw)

def gatherFields(obj):
    fields = {}
    try:
        fields['username'] = obj['username']
        fields['saltpw'] = obj['password']
        fields['client'] = obj['client']
    except Exception as e:
        appendDictasBacktraceAttributes(obj)
        al.log(al.LOG_ERROR,"Error parsing request. {}".format(obj))
        raise e 
        return None

    appendDictasBacktraceAttributes(fields)
    return fields

@app.route('/login', methods=['GET', 'POST'])
def loginHandler():
    token = -1
    errorResponse = ("{ \"msg\": \"Auth Failure\" }", 400)

    if request.method == "GET":
        f = open("static/index.html", "r")
        return f.read()

    try: 
        payload = json.loads(request.data)
    except Exception as e:
        al.sendErrror(e)
        return errorResponse
    
    appendObjBacktraceAttibutes("request", request.data)
    fields = gatherFields(payload)
    if fields is None:
        return errorResponse

    if authenticateUser(fields['username'], fields['saltpw']) is False:
        return errorResponse

    try:
        al.trackingLog(fields['username'], fields['client'])
    except Exception as e:
        handleError(e)

    token = al.generateSession(payload['username'])
    al.log(al.LOG_INFO, "username {} authenticated. {}".format(payload['username'], token))
    return token, 200
    
@app.route('/favicon.ico') 
def favicon(): 
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__== '__main__':
    app.run(host='0.0.0.0', port=80)
