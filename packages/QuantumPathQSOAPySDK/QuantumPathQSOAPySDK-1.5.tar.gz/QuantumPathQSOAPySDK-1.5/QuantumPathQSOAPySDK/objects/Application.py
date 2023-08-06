class Application:

    # CONSTRUCTOR
    def __init__(self, applicationName: str, idSolution: int, idFlow: int, idDevice: int, executionToken: str):
        self.__applicationName = applicationName
        self.__idSolution = idSolution
        self.__idFlow = idFlow
        self.__idDevice = idDevice
        self.__executionToken = executionToken


    # GETTERS
    def getApplicationName(self) -> str:
        return self.__applicationName

    def getIdSolution(self) -> int:
        return self.__idSolution

    def getIdFlow(self) -> int:
        return self.__idFlow

    def getIdDevice(self) -> int:
        return self.__idDevice

    def getExecutionToken(self) -> str:
        return self.__executionToken