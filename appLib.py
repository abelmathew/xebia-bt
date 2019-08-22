#appLib.py

from . import userStore as userStore
passwords = {
    "amathew": "salted",
    "vlussenberg": "salted2"
}

def trackingLog(username, appversion):
    userStore.write( { "username": username, "appversion": appversion } )
    return

def generateSession(username):
    return { "token": "lildjf1093l23923" }

def checkPassword(username, saltpw):
    if username in passwords:
        return passwords[username] == saltpw

    return False

LOG_LEVEL=-1
LOG_INFO=1
def log(level, string):
    if level == LOG_LEVEL:
        print string
    return

