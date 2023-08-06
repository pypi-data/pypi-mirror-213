class AssetManagementResult:

    # CONSTRUCTOR
    def __init__(self, assetManagementResult: dict):
        self.__exitCode = assetManagementResult['ExitCode']
        self.__exitMessage = assetManagementResult['ExitMessage']

        self.__lifecycleToken = assetManagementResult['AssetData']['LifecycleToken']
        self.__idSolution = assetManagementResult['AssetData']['SolutionID']
        self.__idAsset = assetManagementResult['AssetData']['AssetID']
        self.__assetName = assetManagementResult['AssetData']['AssetName']
        self.__assetNamespace = assetManagementResult['AssetData']['AssetNamespace']
        self.__assetType = assetManagementResult['AssetData']['AssetType']
        self.__assetLevel = assetManagementResult['AssetData']['AssetLevel']
        self.__assetCompiledStatus = assetManagementResult['AssetData']['IsCompiled']
        self.__assetTranspiledStatus = assetManagementResult['AssetData']['IsTranspiled']


    # GETTERS
    def getExitCode(self) -> str:
        return self.__exitCode

    def getExitMessage(self) -> str:
        return self.__exitMessage

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