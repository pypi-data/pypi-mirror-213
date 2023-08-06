import unittest
from QuantumPathQSOAPySDK import QSOAPlatform
from .test_QSOAPlatform import (
    waitForApplicationResponse,
    idSolution_gates,
    idDevice_gates,
    idFlow_gates,
    executionToken_gates,
    idSolution_annealing,
    idFlow_annealing,
    executionToken_annealing
)

##################_____GET VERSION_____##################
class Test_GetVersion(unittest.TestCase):

    # GET VERSION
    def test_getVersion(self):
        qsoa = QSOAPlatform(configFile=True)

        version = qsoa.getVersion()

        self.assertIsInstance(version, str)

    # NOT LOGGED IN
    def test_getVersion_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getVersion()
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET LICENCE INFO_____##################
class Test_LicenceInfo(unittest.TestCase):

    # GET LICENCE INFO
    def test_getLlicenceInfo(self):
        qsoa = QSOAPlatform(configFile=True)

        version = qsoa.getLicenceInfo()

        self.assertIsInstance(version, dict)

    # NOT LOGGED IN
    def test_getLlicenceInfo_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getLicenceInfo()
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM SOLUTION LIST_____##################
class Test_GetQuantumSolutionList(unittest.TestCase):

    # GET QUANTUM SOLUTION LIST
    def test_getQuantumSolutionList(self):
        qsoa = QSOAPlatform(configFile=True)

        solutionList = qsoa.getQuantumSolutionList()

        self.assertIsInstance(solutionList, dict)

    # NOT LOGGED IN
    def test_getQuantumSolutionList_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumSolutionList()
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM SOLUTIONS_____##################
class Test_GetQuantumSolutions(unittest.TestCase):

    # GET QUANTUM SOLUTIONS
    def test_getQuantumSolutions(self):
        qsoa = QSOAPlatform(configFile=True)

        solutions = qsoa.getQuantumSolutions()

        self.assertIsInstance(solutions, list)

        firstSolution = solutions[0]
        self.assertEqual(type(firstSolution).__name__, 'SolutionItem')

    # NOT LOGGED IN
    def test_getQuantumSolutions_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumSolutions()
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM SOLUTION NAME_____##################
class Test_GetQuantumSolutionName(unittest.TestCase):

    # GET QUANTUM SOLUTION NAME
    def test_getQuantumSolutionName(self):
        qsoa = QSOAPlatform(configFile=True)

        solutionName = qsoa.getQuantumSolutionName(idSolution_gates)

        self.assertIsInstance(solutionName, str)

    # BAD ARGUMENT idSolution
    def test_getQuantumSolutionName_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumSolutionName(99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumSolutionName_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumSolutionName('idSolution')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumSolutionName_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumSolutionName(idSolution_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM DEVICE LIST_____##################
class Test_GetQuantumDeviceList(unittest.TestCase):

    # GET QUANTUM DEVICE LIST
    def test_getQuantumDeviceList(self):
        qsoa = QSOAPlatform(configFile=True)

        deviceList = qsoa.getQuantumDeviceList(idSolution_gates)

        self.assertIsInstance(deviceList, dict)

    # BAD ARGUMENT idSolution
    def test_getQuantumDeviceList_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumDeviceList(99)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumDeviceList_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        idSolution = 'id'

        try:
            qsoa.getQuantumDeviceList('idSolution')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumDeviceList_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumDeviceList(idSolution_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM DEVICES_____##################
class Test_GetQuantumDevices(unittest.TestCase):

    # GET QUANTUM DEVICES
    def test_getQuantumDevices(self):
        qsoa = QSOAPlatform(configFile=True)

        devices = qsoa.getQuantumDevices(idSolution_gates)

        self.assertIsInstance(devices, list)

        firstDevice = devices[0]
        self.assertEqual(type(firstDevice).__name__, 'DeviceItem')

    # BAD ARGUMENT idSolution
    def test_getQuantumDevices_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumDevices(9)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumDevices_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumDevices('idSolution')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumDevices_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumDevices(idSolution_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM DEVICE NAME_____##################
class Test_GetQuantumDeviceName(unittest.TestCase):

    # GET QUANTUM DEVICE NAME
    def test_getQuantumDeviceName(self):
        qsoa = QSOAPlatform(configFile=True)

        deviceName = qsoa.getQuantumDeviceName(idSolution_gates, idDevice_gates)

        self.assertIsInstance(deviceName, str)

    # BAD ARGUMENT idSolution
    def test_getQuantumDeviceName_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumDeviceName(99, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
    
    # BAD ARGUMENT idDevice
    def test_getQuantumDeviceName_badArgument_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumDeviceName(idSolution_gates, 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumDeviceName_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumDeviceName('idSolution', idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE idDevice
    def test_getQuantumDeviceName_badArgumentType_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumDeviceName(idSolution_gates, 'idDevice')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumDeviceName_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumDeviceName(idSolution_gates, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM FLOW LIST_____##################
class Test_GetQuantumFlowList(unittest.TestCase):

    # GET QUANTUM FLOW LIST
    def test_getQuantumFlowList(self):
        qsoa = QSOAPlatform(configFile=True)

        flowList = qsoa.getQuantumFlowList(idSolution_gates)

        self.assertIsInstance(flowList, dict)

    # BAD ARGUMENT idSolution
    def test_getQuantumFlowList_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumFlowList(99)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumFlowList_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumFlowList('idSolution')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumFlowList_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumFlowList(idSolution_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM FLOWS_____##################
class Test_GetQuantumFlows(unittest.TestCase):

    # GET QUANTUM FLOWS
    def test_getQuantumFlows(self):
        qsoa = QSOAPlatform(configFile=True)

        flows = qsoa.getQuantumFlows(idSolution_gates)

        self.assertIsInstance(flows, list)

        firstFlow = flows[0]
        self.assertEqual(type(firstFlow).__name__, 'FlowItem')

    # BAD ARGUMENT idSolution
    def test_getQuantumFlows_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumFlows(99)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumFlows_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumFlows('idSolution')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumFlows_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumFlows(idSolution_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM FLOW NAME_____##################
class Test_GetQuantumFlowName(unittest.TestCase):

    # GET QUANTUM FLOW NAME
    def test_getQuantumFlowName(self):
        qsoa = QSOAPlatform(configFile=True)

        flowName = qsoa.getQuantumFlowName(idSolution_gates, idFlow_gates)

        self.assertIsInstance(flowName, str)

    # BAD ARGUMENT idSolution
    def test_getQuantumFlowName_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumFlowName(00, idFlow_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
    
    # BAD ARGUMENT idFlow
    def test_getQuantumFlowName_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumFlowName(idSolution_gates, 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumFlowName_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumFlowName('idSolution', idFlow_gates)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE idFlow
    def test_getQuantumFlowName_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumFlowName(idSolution_gates, 'idFlow')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumFlowName_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumFlowName(idSolution_gates, idFlow_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____RUN QUANTUM APPLICATION_____##################
class Test_RunQuantumApplication(unittest.TestCase):

    # RUN QUANTUM APPLICATION
    def test_runQuantumApplication(self):
        qsoa = QSOAPlatform(configFile=True)

        application = qsoa.runQuantumApplication('ApplicationName', idSolution_gates, idFlow_gates, idDevice_gates)
        waitForApplicationResponse(qsoa, application)

        self.assertEqual(type(application).__name__, 'Application')

    # BAD ARGUMENT idSolution
    def test_runQuantumApplication_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplication('ApplicationName', 99, idFlow_gates, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
    
    # BAD ARGUMENT idFlow
    def test_runQuantumApplication_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplication('ApplicationName', idSolution_gates, 99, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT idDevice
    def test_runQuantumApplication_badArgument_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplication('ApplicationName', idSolution_gates, idFlow_gates, 99)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE applicationName
    def test_runQuantumApplication_badArgumentType_applicationName(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplication(99, idSolution_gates, idFlow_gates, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE idSolution
    def test_runQuantumApplication_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplication('ApplicationName', 'idSolution', idFlow_gates, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    
    # BAD ARGUMENT TYPE idFlow
    def test_runQuantumApplication_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplication('ApplicationName', idSolution_gates, 'idFlow', idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE idDevice
    def test_runQuantumApplication_badArgumentType_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplication('ApplicationName', idSolution_gates, idFlow_gates, 'idDevice')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_runQuantumApplication_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.runQuantumApplication('ApplicationName', idSolution_gates, idFlow_gates, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____RUN QUANTUM APPLICATION SYNC_____##################
class Test_RunQuantumApplicationSync(unittest.TestCase):

    # RUN QUANTUM APPLICATION SYNC
    def test_runQuantumApplicationSync(self):
        qsoa = QSOAPlatform(configFile=True)

        application = qsoa.runQuantumApplicationSync('ApplicationName', idSolution_gates, idFlow_gates, idDevice_gates)

        self.assertEqual(type(application).__name__, 'Application')

    # BAD ARGUMENT idSolution
    def test_runQuantumApplicationSync_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplicationSync('ApplicationName', 99, idFlow_gates, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
    
    # BAD ARGUMENT idFlow
    def test_runQuantumApplicationSync_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplicationSync('ApplicationName', idSolution_gates, 99, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT idDevice
    def test_runQuantumApplicationSync_badArgument_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplicationSync('ApplicationName', idSolution_gates, idFlow_gates, 99)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE applicationName
    def test_runQuantumApplicationSync_badArgumentType_applicationName(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplicationSync(99, idSolution_gates, idFlow_gates, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE idSolution
    def test_runQuantumApplicationSync_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplicationSync('ApplicationName', 'idSolution', idFlow_gates, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    
    # BAD ARGUMENT TYPE idFlow
    def test_runQuantumApplicationSync_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplicationSync('ApplicationName', idSolution_gates, 99, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idDevice
    def test_runQuantumApplicationSync_badArgumentType_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.runQuantumApplicationSync('ApplicationName', idSolution_gates, idFlow_gates, 'idDevice')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_runQuantumApplicationSync_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.runQuantumApplicationSync('ApplicationName', idSolution_gates, idFlow_gates, idDevice_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM EXECUTION RESPONSE_____##################
class Test_GetQuantumExecutionResponse(unittest.TestCase):

    # GET QUANTUM EXECTUTION RESPONSE APPLICATION OBJECT
    def test_getQuantumExecutionResponse_applicationObject(self):
        qsoa = QSOAPlatform(configFile=True)

        application = qsoa.runQuantumApplicationSync('ApplicationName', idSolution_gates, idFlow_gates, idDevice_gates)

        execution = qsoa.getQuantumExecutionResponse(application)

        self.assertEqual(type(execution).__name__, 'Execution')

    # GET QUANTUM EXECTUTION RESPONSE EXECUTION TOKEN
    def test_getQuantumExecutionResponse_executionToken(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        self.assertEqual(execution.getExitCode(), 'OK')

    # EXECUTION TOKEN BAD ARGUMENT executionToken
    def test_getQuantumExecutionResponse_executionToken_badArgument_executionToken(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse('executionToken', idSolution_gates, idFlow_gates)

        self.assertEqual(execution.getExitCode(), 'ERR')

    # EXECUTION TOKEN BAD ARGUMENT idSolution
    def test_getQuantumExecutionResponse_executionToken_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, 99, idFlow_gates)

        self.assertEqual(execution.getExitCode(), 'ERR')

    # EXECUTION TOKEN BAD ARGUMENT idFlow
    def test_getQuantumExecutionResponse_executionToken_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, 99)

        self.assertEqual(execution.getExitCode(), 'ERR')

    # APPLICATION OBJECT BAD ARGUMENT TYPE application
    def test_getQuantumExecutionResponse_applicationObject_badArgumentType_application(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionResponse(99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # EXECUTION TOKEN BAD ARGUMENT TYPE executionToken
    def test_getQuantumExecutionResponse_executionToken_badArgumentType_executionToken(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionResponse(99, idSolution_gates, idFlow_gates)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # EXECUTION TOKEN BAD ARGUMENT TYPE idSolution
    def test_getQuantumExecutionResponse_executionToken_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionResponse(executionToken_gates, 'idSolution', idFlow_gates)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # EXECUTION TOKEN BAD ARGUMENT TYPE idFlow
    def test_getQuantumExecutionResponse_executionToken_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, 'idFlow')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumExecutionResponse_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____REPRESENT RESULTS_____##################
class Test_RepresentResults(unittest.TestCase):

    # REPRESENT RESULTS GATES
    def test_representResults_gates(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        representation = qsoa.representResults(execution)

        self.assertIsNone(representation)

    # REPRESENT RESULTS GATES RESULT INDEX
    def test_representResults_gates_resultIndex(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        representation = qsoa.representResults(execution, 0)

        self.assertIsNone(representation)
    
    # REPRESENT RESULTS ANNEALING
    def test_representResults_annealing(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_annealing, idSolution_annealing, idFlow_annealing)

        representation = qsoa.representResults(execution)

        self.assertIsInstance(representation, str)

    # REPRESENT RESULTS ANNEALING RESULT INDEX
    def test_representResults_annealing_resultIndex(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_annealing, idSolution_annealing, idFlow_annealing)

        representation = qsoa.representResults(execution, 0)

        self.assertIsInstance(representation, str)

    # BAD ARGUMENT execution
    def test_representResults_badArgument_execution(self):
        qsoa = QSOAPlatform(configFile=True)

        executionToken = 'be2b3021-d294-472e-8265-3b39583ad172'
        execution = qsoa.getQuantumExecutionResponse(executionToken, idSolution_gates, idFlow_gates)

        try:
            qsoa.representResults(execution)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ExecutionObjectError')
            
    # BAD ARGUMENT resultIndex
    def test_representResults_badArgument_resultIndex(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        try:
            qsoa.representResults(execution, 1)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'IndexError')

    # BAD ARGUMENT TYPE execution
    def test_representResults_badArgumentType_execution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.representResults(99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE resultIndex
    def test_representResults_badArgumentType_resultIndex(self):
        qsoa = QSOAPlatform(configFile=True)

        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)

        try:
            qsoa.representResults(execution, 'resultIndex')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_representResults_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)
        execution = qsoa.getQuantumExecutionResponse(executionToken_gates, idSolution_gates, idFlow_gates)
        qsoa = QSOAPlatform()

        try:
            qsoa.representResults(execution)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


if __name__ == '__main__':
    unittest.main()