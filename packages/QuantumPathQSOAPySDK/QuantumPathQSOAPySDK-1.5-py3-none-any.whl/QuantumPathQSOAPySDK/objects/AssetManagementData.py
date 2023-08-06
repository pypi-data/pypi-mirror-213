class AssetManagementData:

    # CONSTRUCTOR
    def __init__(self, assetManagementData: dict):
        self.__lifecycleToken = assetManagementData['LifecycleToken']
        self.__idSolution = assetManagementData['SolutionID']
        self.__idAsset = assetManagementData['AssetID']
        self.__assetName = assetManagementData['AssetName']
        self.__assetNamespace = assetManagementData['AssetNamespace']
        self.__assetType = assetManagementData['AssetType']
        self.__assetLevel = assetManagementData['AssetLevel']
        self.__assetCompiledStatus = assetManagementData['IsCompiled']
        self.__assetTranspiledStatus = assetManagementData['IsTranspiled']


    # GETTERS
    def getLifecycleToken(self) -> str:
        return self.__lifecycleToken
    
    def getIdSolution(self) -> int:
        return self.__idSolution
    
    def getIdAsset(self) -> int:
        return self.__idAsset
    
    def getAssetName(self) -> str:
        return self.__assetName
    
    def getAssetNamespace(self) -> str:
        return self.__assetNamespace
    
    def getAssetType(self) -> str:
        return self.__assetType
    
    def getAssetLevel(self) -> str:
        return self.__assetLevel
    
    def getAssetCompiledStatus(self) -> bool:
        return self.__assetCompiledStatus
    
    def getAssetTranspiledStatus(self) -> bool:
        return self.__assetTranspiledStatus