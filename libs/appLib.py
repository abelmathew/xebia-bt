#appLib.py

from . import userStore as userStore
passwords = {
    "amathew": "****",
    "vlussenberg": "****"
}

def trackingLog(username, appversion):
    userStore.write( { "username": username, "appversion": appversion } )
    return

def generateSession(username):
    return { "sessionID": "lildjf1093l23923" }

def checkPassword(username, saltpw):
    if username in passwords:
        return passwords[username] == saltpw

    return False

LOG_LEVEL=-1
LOG_INFO=1
LOG_WARNING=2
LOG_ERROR=3
LOG_CRITICAL=4
def log(level, string):
    if level == LOG_LEVEL:
        print string
    return

