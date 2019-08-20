#!/usr/bin/env python

##
# TODO: 
# 
## 

import sys, os
import random

#insert file into path for code capture
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, root_dir)
import backtracepython as bt

from flask import Flask
app = Flask(__name__)

# initializing Backtrace after Flask for ease of use
@app.route('/init')
def init():
    bt.initialize(
            endpoint="https://submit.backtrace.io/testing-xebialabs/e958cfd2940e7bdb2d60fdf7fd22d4caaecdb9966efc835e24054a247aef6162/json",
            token="e958cfd2941e7bdb2d60fdf7fd22d4caaecdb9966efc835e24054a247aef6162",
            context_line_count=3
            )
    return "initialized"

# Flask overrides global exception handler. errorhandler allows us to rewrite it
@app.errorhandler(Exception)
def handle_error(e):
    report = bt.BacktraceReport()
    report.capture_last_exception()
    report.send()
    return "Error Encountered."

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

def main():
    app.run()

if __name__== '__main__':
    main()
