class DeviceItem:

    # CONSTRUCTOR
    def __init__(self, device: dict):
        self.__deviceShortName = device['DeviceShortName']
        self.__quantumMachineType = device['QuantumMachineType']
        self.__isLocalSimulator = device['IsLocalSimulator']
        self.__idVendor = device['idVendor'] ################################## idDevice
        self.__vendorName = device['VendorName']
        self.__description = device['Description']
        self.__deviceName = device['DeviceName']
    
    
    # GETTERS
    def getDeviceShortName(self) -> str:
        return self.__deviceShortName

    def getQuantumMachineType(self) -> str:
        return self.__quantumMachineType
        
    def getIsLocalSimulator(self) -> bool:
        return self.__isLocalSimulator

    def getIdVendor(self) -> int:
        return self.__idVendor

    def getVendorName(self) -> str:
        return self.__vendorName

    def getDescription(self) -> str:
        return self.__description

    def getDeviceName(self) -> str:
        return self.__deviceName