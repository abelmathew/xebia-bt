#!/usr/bin/env python

import sys, os
import random
import json

#insert file into path for code capture
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, root_dir)
import backtracepython as bt

from flask import Flask


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

# initializing Backtrace after Flask for ease of use
@app.route('/init')
def init():
    return "initialized"

# Flask overrides global exception handler. errorhandler allows us to rewrite it
@app.errorhandler(Exception)
def handle_error(e):
    report = bt.BacktraceReport()
    report.capture_last_exception()
    report.send()
    return json.dumps(globalAttributes)

@app.route('/')
def index():
    return "\n"

def crashNestedFunction():
    a = b
    return

def crash():
    print "nested function"
    local_var = random.random()
    crashNestedFunction()
    return

@app.route('/crash')
def crashHandler():
    crash()
    return "Hello World!"

if __name__== '__main__':
    app.run()
