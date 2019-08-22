#userStore.py

import io
import sys
import time

def dummyFailure():
    #failure to open
    raise IOError("Connection to DB failed: BacktraceDatabase cannot be resolved")
    return

def write(payload):
    obj = {}
    obj["timestamp"] = time.time()
    for key in payload.keys():
        obj[key] = payload[key]

    dummyFailure()

    return
    
