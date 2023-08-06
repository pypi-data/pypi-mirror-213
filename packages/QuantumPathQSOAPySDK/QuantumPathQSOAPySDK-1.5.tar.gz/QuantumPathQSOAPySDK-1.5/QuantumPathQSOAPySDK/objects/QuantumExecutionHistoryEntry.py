class QuantumExecutionHistoryEntry:

    # CONSTRUCTOR
    def __init__(self, quantumExecutionHistoryEntry: dict):
        self.__idResult = quantumExecutionHistoryEntry['IdResult']
        self.__idSolution = quantumExecutionHistoryEntry['IdSolution']
        self.__solutionName = quantumExecutionHistoryEntry['SolutionName']
        self.__idFlow = quantumExecutionHistoryEntry['IdFlow']
        self.__flowName = quantumExecutionHistoryEntry['FlowName']
        self.__idDevice = quantumExecutionHistoryEntry['IdDevice']
        self.__deviceName = quantumExecutionHistoryEntry['DeviceName']
        self.__deviceShortName = quantumExecutionHistoryEntry['DeviceShortName']
        self.__deviceVendor = quantumExecutionHistoryEntry['DeviceVendor']
        self.__isLocalSimulator = quantumExecutionHistoryEntry['IsLocalSimulator']
        self.__deviceTypeName = quantumExecutionHistoryEntry['DeviceTypeName']
        self.__resultHistogram = quantumExecutionHistoryEntry['ResultHistogram']
        self.__executionDate = quantumExecutionHistoryEntry['ExecutionDate']
        self.__durationMinutes = quantumExecutionHistoryEntry['DurationMinutes']
        self.__resultType = quantumExecutionHistoryEntry['ResultType']
        self.__resultDescription = quantumExecutionHistoryEntry['ResultDescription']
        

    # GETTERS
    def getIdResult(self) -> int:
        return self.__idResult
        
    def getIdSolution(self) -> int:
        return self.__idSolution

    def getSolutionName(self) -> str:
        return self.__solutionName
        
    def getIdFlow(self) -> int:
        return self.__idFlow

    def getFlowName(self) -> str:
        return self.__flowName

    def getIdDevice(self) -> int:
        return self.__idDevice

    def getDeviceName(self) -> str:
        return self.__deviceName
        
    def getDeviceShortName(self) -> str:
        return self.__deviceShortName

    def getDeviceVendor(self) -> str:
        return self.__deviceVendor

    def getIsLocalSimulator(self) -> bool:
        return self.__isLocalSimulator

    def getDeviceTypeName(self) -> str:
        return self.__deviceTypeName
        
    def getResultHistogram(self) -> str:
        return self.__resultHistogram

    def getExecutionDate(self) -> float:
        return self.__executionDate

    def getDurationMinutes(self) -> float:
        return self.__durationMinutes

    def getResultType(self) -> str:
        return self.__resultType

    def getResultDescription(self) -> str:
        return self.__resultDescription