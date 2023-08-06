from ..utils.apiConnection import apiConnection
from ..utils.Exception import (ConfigFileError, Base64Error)

import base64
import hashlib
from pathlib import Path
from configparser import ConfigParser

# API ENDPOINTS
securityEndpoints = {
    'echoping': 'login/echoping/',
    'echouser': 'login/echouser/',
    'echostatus': 'login/echostatus',
    'authenticate': 'login/authenticate/',
    'authenticateEx': 'login/authenticateEx/'
}

# PRIVATE METHODS
def __getCredentialsFromConfigFile(context) -> list:
    try:
        qpathcredentials = ConfigParser(allow_no_value=True)
        qpathcredentials.read(str(Path.home()) + '\.qpath')

        username = qpathcredentials[context.getActiveEnvironment()[1] + '-credentials']['username']
        password = qpathcredentials[context.getActiveEnvironment()[1] + '-credentials']['password']

    except:
        raise ConfigFileError('Error reading username or password in config file')
    
    return [username, password]

def __decodePassword(password: str) -> str:
    try:
        return base64.b64decode(password).decode('utf-8')
    
    except:
        raise Base64Error('Invalid Base64 encoding in password')

def __getURL(context) -> str:
    return context.getEnvironments()[context.getActiveEnvironment()[0]][context.getActiveEnvironment()[1]]


##################_____SECURITY METHODS_____##################

# ENCODE PASSWORD
def encodePassword(self, password: str):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    encoded_password = encoded_bytes.decode('utf-8')

    return encoded_password

# ENCRYPT PASSWORD
def encryptPassword(self, password: str):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    return hashed_password

# AUTHENTICATE BASIC
def authenticateBasic(self, context, username: str = None, password: str = None) -> bool:
    url = __getURL(context) + securityEndpoints['authenticate']

    if not username and not password:
        credentials = __getCredentialsFromConfigFile(context)
        username = credentials[0]
        password = credentials[1]

    elif not username or not password:
        raise ValueError('QSOAPlatform.authenticateBasic() takes from 1 to 3 positional arguments')

    context.updateContext(username, password, url)

    return True

# AUTHENTICATE
def authenticate(self, context, username: str = None, password: str = None) -> bool:
    url = __getURL(context) + securityEndpoints['authenticate']

    if not username and not password:
        credentials = __getCredentialsFromConfigFile(context)
        username = credentials[0]
        password = credentials[1]
        
    elif not username or not password:
        raise ValueError('QSOAPlatform.authenticate() takes from 1 to 3 positional arguments')

    else:
        password = __decodePassword(password)

    context.updateContext(username, password, url)

    return True

# AUTHENTICATE EX
def authenticateEx(self, context, username: str = None, password: str = None) -> bool:
    url = __getURL(context) + securityEndpoints['authenticateEx']

    if not username and not password:
        credentials = __getCredentialsFromConfigFile(context)
        username = credentials[0]
        password = credentials[1]

    elif not username or not password:
        raise ValueError('QSOAPlatform.authenticateEx() takes from 1 to 3 positional arguments')

    context.updateContext(username, password, url)

    return True

# ECHOPING
def echoping(self, context) -> bool:
    url = __getURL(context) + securityEndpoints['echoping']
    
    return apiConnection(url, 'boolean')

# ECHOSTATUS
def echostatus(self, context) -> bool:
    url = __getURL(context) + securityEndpoints['echostatus']

    return apiConnection(url, context.getHeader(), 'boolean')

# ECHOUSER
def echouser(self, context) -> str:
    url = __getURL(context) + securityEndpoints['echouser']

    return apiConnection(url, context.getHeader(), 'string')