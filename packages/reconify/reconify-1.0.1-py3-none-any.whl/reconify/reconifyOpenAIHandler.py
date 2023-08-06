import time
import requests
import json

#constants
RECONIFY_TRACKER = 'https://track.reconify.com/track';

#private variables 
__appKey = None
__apiKey = None
__debug = False
__tracker = RECONIFY_TRACKER
__user = {}
__session = ''
__sessionTimeout = ''

def __logInteraction(input, output, timestampIn, timestampOut, type):
    if __debug:
        print('Logging interaction')
    payload = {
        "reconify" :{
            "format": 'openai',
            "appKey": __appKey,
            "apiKey": __apiKey,
            "type": type,
            "version": '1.0.0',
        },
        "request": input,
        "response": output,
        "user": __user,
        "session": __session,
        "sessionTimeout": __sessionTimeout,
        "timestamps": {
            "request": timestampIn,
            "response": timestampOut
        },
    }
    if __debug:
        print('Sending payload: ', payload)
    try:
        requests.post(__tracker, json=payload)
    except requests.exceptions.RequestException as err:
        if __debug:
            print('Send error: ', err)

    return

def config (openai, appKey, apiKey, **options):
    global __appKey
    global __apiKey
    global __debug
    global __tracker
    global __user
    global __session
    global __sessionTimeout

    __appKey = appKey
    __apiKey = apiKey
    if __appKey is None or __apiKey is None:
        raise Exception('An appKey and apiKey are required')
    #optional overides
    if 'debug' in options and options.get('debug') == True:
        __debug = True

    if 'tracker' in options:
        __tracker = options.get('tracker')

    #override chat create
    openai.ChatCompletion.originalCreate = openai.ChatCompletion.create
    def __reconifyCreateChatCompletion(*args, **kwargs):
        tsIn = round(time.time()*1000)
        response = openai.ChatCompletion.originalCreate(*args, **kwargs)
        tsOut = round(time.time()*1000)
        __logInteraction(kwargs, response, tsIn, tsOut, 'chat')
        return response 
    openai.ChatCompletion.create = __reconifyCreateChatCompletion 

    #override completion create
    openai.Completion.originalCreate = openai.Completion.create
    def __reconifyCreateCompletion(*args, **kwargs):
        tsIn = round(time.time()*1000)
        response = openai.Completion.originalCreate(*args, **kwargs)
        tsOut = round(time.time()*1000)
        __logInteraction(kwargs, response, tsIn, tsOut, 'completion')
        return response 
    openai.Completion.create = __reconifyCreateCompletion
    return

def setUser(user):
    global __user
    __user = user

def setSession(session):
    global __session
    __session = session

def setSessionTimeout(sessionTimeout):
    global __sessionTimeout
    __sessionTimeout = sessionTimeout