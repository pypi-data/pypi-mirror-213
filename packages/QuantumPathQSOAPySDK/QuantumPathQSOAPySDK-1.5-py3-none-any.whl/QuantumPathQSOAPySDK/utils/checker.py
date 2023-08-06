from ..utils.apiConnection import apiConnection
from .Exception import AuthenticationError

import math

def getURL(context) -> str:
    return context.getEnvironments()[context.getActiveEnvironment()[0]][context.getActiveEnvironment()[1]]

def checkUserSession(context):
    url = getURL(context) + 'login/echostatus'

    if not apiConnection(url, context.getHeader(), 'boolean'):
        raise AuthenticationError('User not authenticated')

def checkInputTypes(*args):
    for argTuple in args:
        expextedTypes = str([i.__name__ for i in argTuple[2]]).replace("['", "<").replace(" '", " <").replace("']", ">").replace("',", ">,")

        if type(argTuple[1]) not in argTuple[2]:
            raise TypeError(f'Argument "{argTuple[0]}" expected to be {expextedTypes}, not <{type(argTuple[1]).__name__}>')

def checkValues(*args):
    for argTuple in args:
        expectedValues = str([i for i in argTuple[2]]).replace('[', '').replace(']', '')
        
        if argTuple[1] not in argTuple[2]:
            raise ValueError(f'Argument "{argTuple[0]}" expected to be {expectedValues}, not "{argTuple[1]}"')

def checkMathExpression(arg: str, expression: str):
    try:
        eval(expression)

    except Exception:
        try:
            expression = expression.replace('pi', 'math.pi')
            expression = expression.replace('e', 'math.e')
            expression = expression.replace('tau', 'math.tau')
            eval(expression)

        except Exception:
            raise ValueError(f'{arg} is not a mathematical expression')

def checkDifferentPosition(positions: list):
    if len(positions) != len(set(positions)):
        raise ValueError('Duplicated positions')