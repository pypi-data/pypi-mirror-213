import base64

class Asset:

    # CONSTRUCTOR
    def __init__(self, asset: dict):
        self.__id = asset['AssetID']
        self.__name = asset['AssetName']
        self.__namespace = asset['AssetNamespace']
        self.__description = asset['AssetDescription']
        self.__body = base64.b64decode(asset['AssetBody']).decode('ascii')
        self.__type = asset['AssetType']
        self.__level = asset['AssetLevel']
        self.__lastUpdate = asset['AssetLastUpdate']


    # GETTERS
    def getId(self) -> int:
        return self.__id
    
    def getName(self) -> str:
        return self.__name
    
    def getNamespace(self) -> str:
        return self.__namespace
    
    def getDescription(self) -> str:
        return self.__description
    
    def getBody(self) -> str:
        return self.__body
    
    def getType(self) -> str:
        return self.__type
    
    def getLevel(self) -> str:
        return self.__level
    
    def getLastUpdate(self) -> str:
        return self.__lastUpdate
    

    # SETTERS
    def setName(self, name: str):
        self.__name = name
    
    def setNamespace(self, namespace: str):
        self.__namespace = namespace
    
    def setDescription(self, description: str):
        self.__description = description
    
    def setBody(self, body: str):
        self.__body = body
    
    def setType(self, type: str):
        self.__type = type
    
    def setLevel(self, level: str):
        self.__level = level