import requests
import json
from .Exception import APIConnectionError

def __deserialize(message, outputType): # deserialize function to transform responses into string, boolean or json dictionaries
    if message.ok:
        if outputType == 'string':
            desMessage = message.text.replace('"', '')

        elif outputType == 'boolean':
            if message.text == 'true':
                desMessage = True
            elif message.text == 'false':
                desMessage = False

        elif outputType == 'json':
            desMessage = json.loads(message.content)

            if isinstance(desMessage, str):
                desMessage = json.loads(desMessage)

    else:
        raise APIConnectionError(f'Error {message.status_code} {message.reason}. {message.text}')

    return desMessage

def apiConnection(*args): # manage api calls
    if len(args) == 2: # echoping
        response = __deserialize(requests.get(args[0]), args[1])
    
    elif len(args) == 3: # normal get calls
        response = __deserialize(requests.get(args[0], headers=args[1]), args[2])
    
    elif len(args) == 4: # create context
        response = __deserialize(requests.post(args[0], data=args[1]), args[2])
    
    elif len(args) == 5: # post asset
        args[1].update({'Content-type': 'application/json; charset=utf-8'})
        response = __deserialize(requests.post(args[0], headers=args[1], data=args[2].encode('utf-8')), args[3])
    
    return response