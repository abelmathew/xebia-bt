#!/usr/bin/env python

import sys, os
import random
import json
from flask import Flask, request

#insert file into path for code capture
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, root_dir)
import backtracepython as bt

#local
from . import appLib as al

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
                endpoint="https://submit.backtrace.io/testing-xebialabs/e958cfd2940e7bdb2d60fdf7fd22d4caaecdb9966efc835e24054a247aef6162/json",
                token="e958cfd2941e7bdb2d60fdf7fd22d4caaecdb9966efc835e24054a247aef6162",
                attributes=globalAttributes,
                context_line_count=3
        )
        print "bt_initialized"
    run_on_start()
    return app
app = createApp()

##
# Backtrace by default provides a global exception handler that will do the equivalent of what is seen.
# Flask overrides this but provides the ability to watch for exceptions via errorhandler decorator 
##
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
    
    ##
    # Scenario 0: Normal Login, no app_version
    # Scenario 1: not checking for the existence of app_version
    # Scenario 2: having a subsystem not found, but don't care because that will come in a later check-in
    ##
    if authenticateUser(payload['username'], payload['password']) is False:
        return errorResponse

    token = al.generateSession(payload['username'])
    al.log(al.LOG_INFO, "username {} authenticated. {}".format(payload['username'], token))
    return token, 200
    
if __name__== '__main__':
    app.run()
