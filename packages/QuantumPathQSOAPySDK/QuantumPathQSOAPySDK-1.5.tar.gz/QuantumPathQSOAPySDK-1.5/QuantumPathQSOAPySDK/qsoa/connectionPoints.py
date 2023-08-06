from ..utils.apiConnection import apiConnection
from ..objects.SolutionItem import SolutionItem
from ..objects.DeviceItem import DeviceItem
from ..objects.FlowItem import FlowItem
from ..objects.Application import Application
from ..objects.Execution import Execution

from matplotlib import pyplot as plt
from prettytable import PrettyTable
import collections
import time


# API ENDPOINTS
connectionPoints = {
    'getVersion': 'connectionPoint/getVersion/',
    'getLicenceInfo': 'connectionPoint/getLicenceInfo/',
    'getQuantumSolutions': 'connectionPoint/getQuantumSolutions/',
    'getQuantumDevices': 'connectionPoint/getQuantumDevices/',
    'getQuantumFlows': 'connectionPoint/getQuantumFlows/',
    'runQuantumApplication': 'connectionPoint/runQuantumApplication/',
    'getQuantumExecutionResponse': 'connectionPoint/getQuantumExecutionResponse/',
    'getQuantumDevicesEx': 'connectionPoint/getQuantumDevicesEx/'
}


# PRIVATE METHODS
def __getURL(context) -> str:
    return context.getEnvironments()[context.getActiveEnvironment()[0]][context.getActiveEnvironment()[1]]

def __plotQuantumGatesCircuit(histogramData: dict, name: str): # __plotQuantumGatesCircuit. Returns a plot
    histogramTitle = name
    histogramValues = histogramData[name]

    histogramValues = collections.OrderedDict(sorted(histogramValues.items())) # sort values

    fig, ax = plt.subplots(1, 1)
    ax.bar([ str(i) for i in histogramValues.keys()], histogramValues.values(), color='g')

    ax.set_title(histogramTitle)

    rects = ax.patches
    labels = [list(histogramValues.values())[i] for i in range(len(rects))]

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height+0.01, label, ha='center', va='bottom')

    plt.show()

def __plotAnnealingCircuit(histogramData, name): # __plotAnnealingCircuit. Returns a String
    histogramTitle = name
    histogramValues = histogramData[name]

    histogramValues2 = histogramValues.copy()
    del histogramValues2['fullsample']

    tableResults =PrettyTable(['Name', 'Value'])

    for key, value in histogramValues['fullsample'].items():
        tableResults.add_row([key, value])

    tableInfo = PrettyTable()
    tableInfo.field_names = histogramValues2.keys()
    tableInfo.add_rows([histogramValues2.values()])

    return f'\n\n{histogramTitle}\n{tableInfo}\n{tableResults}'


##################_____STATIC METHODS_____##################

# GET VERSION
def getVersion(self, context) -> str:
    url = __getURL(context) + connectionPoints['getVersion']

    return apiConnection(url, context.getHeader(), 'string')
    
# GET LICENCE INFO
def getLicenceInfo(self, context) -> dict:
    url = __getURL(context) + connectionPoints['getLicenceInfo']

    return apiConnection(url, context.getHeader(), 'json')

# GET QUANTUM SOLUTION LIST
def getQuantumSolutionList(self, context) -> dict:
    url = __getURL(context) + connectionPoints['getQuantumSolutions']
 
    return apiConnection(url, context.getHeader(), 'json')

# GET QUANTUM SOLUTIONS
def getQuantumSolutions(self, context) -> list:
    solutions = list()

    url = __getURL(context) + connectionPoints['getQuantumSolutions']

    solutionsDict = apiConnection(url, context.getHeader(), 'json')

    for idSolution in solutionsDict:
        solutions.append(SolutionItem(int(idSolution), solutionsDict[idSolution]))

    return solutions

# GET QUANTUM SOLUTION NAME
def getQuantumSolutionName(self, context, idSolution: int) -> str:
    url = __getURL(context) + connectionPoints['getQuantumSolutions']

    solutionsDict = apiConnection(url, context.getHeader(), 'json')
    
    if str(idSolution) in solutionsDict.keys():
        solutionName = solutionsDict[str(idSolution)]
    
    else:
        raise ValueError('Incorrect Solution ID')

    return solutionName

# GET QUANTUM DEVICE LIST
def getQuantumDeviceList(self, context, idSolution: int) -> dict:
    url = __getURL(context) + connectionPoints['getQuantumDevices'] + str(idSolution)

    return apiConnection(url, context.getHeader(), 'json')

# GET QUANTUM DEVICES
def getQuantumDevices(self, context, idSolution: int) -> list:
    devices = list()

    url = __getURL(context) + connectionPoints['getQuantumDevicesEx'] + str(idSolution)

    devicesDict = apiConnection(url, context.getHeader(), 'json')

    for device in devicesDict:
        devices.append(DeviceItem(device))
    
    return devices

# GET QUANTUM DEVICE NAME
def getQuantumDeviceName(self, context, idSolution: int, idDevice: int) -> str:
    url = __getURL(context) + connectionPoints['getQuantumDevices'] + str(idSolution)

    devicesDict = apiConnection(url, context.getHeader(), 'json')
    
    if str(idDevice) in devicesDict.keys():
        deviceName = devicesDict[str(idDevice)]
    
    else:
        raise ValueError('Incorrect Device ID')

    return deviceName

# GET QUANTUM FLOW LIST
def getQuantumFlowList(self, context, idSolution: int) -> dict:
    url = __getURL(context) + connectionPoints['getQuantumFlows'] + str(idSolution)
    
    return apiConnection(url, context.getHeader(), 'json')

# GET QUANTUM FLOWS
def getQuantumFlows(self, context, idSolution: int) -> list:
    flows = list()

    url = __getURL(context) + connectionPoints['getQuantumFlows'] + str(idSolution)

    flowsDict = apiConnection(url, context.getHeader(), 'json')

    for idFlow in flowsDict:
        flows.append(FlowItem(int(idFlow), flowsDict[idFlow]))
    
    return flows

# GET QUANTUM FLOW NAME
def getQuantumFlowName(self, context, idSolution: int, idFlow: int) -> str:
    url = __getURL(context) + connectionPoints['getQuantumFlows'] + str(idSolution)

    flowsDict = apiConnection(url, context.getHeader(), 'json')
    
    if str(idFlow) in flowsDict.keys():
        flowName = flowsDict[str(idFlow)]
    
    else:
        raise ValueError('Incorrect Flow ID')

    return flowName

# RUN QUANTUM APPLICATION
def runQuantumApplication(self, context, applicationName: str, idSolution: int, idFlow: int, idDevice: int) -> Application:
    url = __getURL(context) + connectionPoints['runQuantumApplication'] + str(applicationName) + '/' + str(idSolution) + '/' + str(idFlow) + '/' + str(idDevice)

    executionToken = apiConnection(url, context.getHeader(), 'string')

    return Application(applicationName, int(idSolution), int(idFlow), int(idDevice), executionToken)

# RUN QUANTUM APPLICATION SYNC
def runQuantumApplicationSync(self, context, applicationName: str, idSolution: int, idFlow: int, idDevice: int) -> Application:
    application = runQuantumApplication(None, context, applicationName, idSolution, idFlow, idDevice)

    execution = getQuantumExecutionResponse(None, context, application)

    while execution.getExitCode() == 'WAIT':
        time.sleep(1)
        execution = getQuantumExecutionResponse(None, context, application)
    
    return application

# GET QUANTUM EXECUTION RESPONSE
def getQuantumExecutionResponse(self, context, *args) -> Execution:
    if len(args) == 1:
        executionToken = args[0].getExecutionToken()
        idSolution = args[0].getIdSolution()
        idFlow = args[0].getIdFlow()
    
    elif len(args) == 3:
        executionToken = args[0]
        idSolution = args[1]
        idFlow = args[2]

    url = __getURL(context) + connectionPoints['getQuantumExecutionResponse'] + str(executionToken) + '/' + str(idSolution) + '/' + str(idFlow)

    executionDict = apiConnection(url, context.getHeader(), 'json')
    
    return Execution(executionDict)

# REPRESENT RESULTS
def representResults(self, context, execution: Execution, resultIndex: int = None):
    representation = None
    histogramData = execution.getHistogram()

    if 'number_of_samples' in (list(histogramData.values())[0]).keys(): # annealing
        if resultIndex == None:
            representation = ''

            for name in histogramData:
                representation = representation + __plotAnnealingCircuit(histogramData, name)
        
        else:
            if resultIndex > -1 and resultIndex < len(histogramData):
                representation = __plotAnnealingCircuit(histogramData, list(histogramData)[resultIndex])
            
            else:
                raise IndexError(f'Invalid resultIndex. It should be 0 to {len(histogramData) - 1}')

    else: # quantum gates
        if resultIndex == None:
            for name in histogramData:
                __plotQuantumGatesCircuit(histogramData, name)
        else:
            if resultIndex > -1 and resultIndex < len(histogramData):
                __plotQuantumGatesCircuit(histogramData, list(histogramData)[resultIndex])

            else:
                raise IndexError(f'Invalid resultIndex. It should be 0 to {len(histogramData) - 1}')

    return representation