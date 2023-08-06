import unittest
from QuantumPathQSOAPySDK import QSOAPlatform
from .test_QSOAPlatform import (
    idSolution_gates,
    idFlow_gates,
    idSolution_annealing,
    idAsset,
    assetName_circuit,
    assetName_flow,
    assetDescription,
    assetNamespace,
    assetBody
)


##################_____GET ASSET CATALOG_____##################
class Test_GetAssetCatalog(unittest.TestCase):

    # GET ASSET CATALOG
    def test_getAssetCatalog(self):
        qsoa = QSOAPlatform(configFile=True)

        assetCatalog = qsoa.getAssetCatalog(idSolution_gates, 'CIRCUIT', 'VL')

        self.assertIsInstance(assetCatalog, list)

        firstAsset = assetCatalog[0]
        self.assertEqual(type(firstAsset).__name__, 'Asset')

    # BAD ARGUMENT idSolution
    def test_getAssetCatalog_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAssetCatalog(99, 'CIRCUIT', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetType
    def test_getAssetCatalog_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAssetCatalog(idSolution_gates, 'assetType', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT assetLevel
    def test_getAssetCatalog_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAssetCatalog(idSolution_gates, 'CIRCUIT', 'assetLevel')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE idSolution
    def test_getAssetCatalog_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAssetCatalog('idSolution', 'CIRCUIT', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetType
    def test_getAssetCatalog_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAssetCatalog(idSolution_gates, 99, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetLevel
    def test_getAssetCatalog_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAssetCatalog(idSolution_gates, 'CIRCUIT', 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getAssetCatalog_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getAssetCatalog(idSolution_gates, 'CIRCUIT', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET ASSET_____##################
class Test_GetAsset(unittest.TestCase):

    # GET ASSET
    def test_getAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        asset = qsoa.getAsset(idAsset, 'CIRCUIT', 'VL')

        self.assertEqual(type(asset).__name__, 'Asset')

    # BAD ARGUMENT idAsset
    def test_getAsset_badArgument_idAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAsset(99, 'CIRCUIT', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetType
    def test_getAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAsset(idAsset, 'assetType', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT assetLevel
    def test_getAsset_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAsset(idAsset, 'CIRCUIT', 'assetLevel')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE idAsset
    def test_getAsset_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAsset('idAsset', 'CIRCUIT', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetType
    def test_getAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAsset(idAsset, 99, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetLevel
    def test_getAsset_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAsset(idAsset, 'CIRCUIT', 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getAsset_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getAsset(idAsset, 'CIRCUIT', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____CREATE ASSET_____##################
class Test_CreateAsset(unittest.TestCase):

    # CREATE ASSET assetBody STRING
    def test_createAsset_assetBody_string(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL'))

    # CREATE ASSET assetBody CIRCUITGATES
    def test_createAsset_assetBody_circuitGates(self):
        qsoa = QSOAPlatform(configFile=True)

        circuit = qsoa.CircuitGates()
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure()

        assetBody = circuit

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL'))

    # CREATE ASSET assetBody CIRCUITANNEALING
    def test_createAsset_assetBody_circuitAnnealing(self):
        qsoa = QSOAPlatform(configFile=True)

        circuit = qsoa.CircuitAnnealing()
        circuit.addParameter([circuit.Parameter('Parametro', 3), circuit.Parameter('Parameter', 1)])

        assetBody = circuit

        assetManagementData = qsoa.createAsset(idSolution_annealing, assetName_circuit, assetNamespace, assetDescription, assetBody, 'ANNEAL', 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL'))

    # CREATE ASSET assetBody CIRCUITFLOW
    def test_createAsset_assetBody_circuitFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        flow = qsoa.CircuitFlow()
        startNode = flow.startNode()
        circuitNode = flow.circuitNode('circuit')
        endNode = flow.endNode()
        flow.linkNodes(startNode, circuitNode)
        flow.linkNodes(circuitNode, endNode)

        assetBody = flow

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_flow, assetNamespace, assetDescription, assetBody, 'FLOW', 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))

    # CREATE ASSET EXISTING ASSET
    def test_createAsset_existingAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL'))

    # BAD ARGUMENT idSolution
    def test_createAsset_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset(99, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetType
    def test_createAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'assetType', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT assetLevel
    def test_createAsset_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'assetLevel')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE idSolution
    def test_createAsset_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset('idSolution', assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetName
    def test_createAsset_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset(idSolution_gates, 99, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetNamespace
    def test_createAsset_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, 99, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetDescription
    def test_createAsset_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, 99, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetBody
    def test_createAsset_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, 99, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetType
    def test_createAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 99, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetLevel
    def test_createAsset_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_createAsset_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____CREATE ASSET SYNC_____##################
class Test_CreateAssetSync(unittest.TestCase):

    # CREATE ASSET SYNC assetBody STRING
    def test_createAssetSync_assetBody_string(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL'))

    # CREATE ASSET SYNC assetBody CIRCUITGATES
    def test_createAssetSync_assetBody_circuitGates(self):
        qsoa = QSOAPlatform(configFile=True)

        circuit = qsoa.CircuitGates()
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure()

        assetBody = circuit

        assetManagementData = qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL'))

    # CREATE ASSET SYNC assetBody CIRCUITFLOW
    def test_createAssetSync_assetBody_circuitFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        flow = qsoa.CircuitFlow()
        startNode = flow.startNode()
        circuitNode = flow.circuitNode('circuit')
        endNode = flow.endNode()
        flow.linkNodes(startNode, circuitNode)
        flow.linkNodes(circuitNode, endNode)

        assetBody = flow

        assetManagementData = qsoa.createAssetSync(idSolution_gates, assetName_flow, assetNamespace, assetDescription, assetBody, 'FLOW', 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))

    # CREATE ASSET SYNC EXISTING ASSET
    def test_createAsset_existingAsset(self):
        qsoa = QSOAPlatform(configFile=True)


        assetManagementData = qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL'))

    # BAD ARGUMENT idSolution
    def test_createAssetSync_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(99, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetNamespace
    def test_createAssetSync_badArgument_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, 99, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT assetType
    def test_createAssetSync_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'assetType', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT assetLevel
    def test_createAssetSync_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'assetLevel')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE idSolution
    def test_createAssetSync_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync('idSolution', assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetName
    def test_createAssetSync_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(idSolution_gates, 99, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetNamespace
    def test_createAssetSync_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, 99, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetDescription
    def test_createAssetSync_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, 99, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetBody
    def test_createAssetSync_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, 99, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetType
    def test_createAssetSync_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 99, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetLevel
    def test_createAssetSync_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_createAssetSync_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.createAssetSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____CREATE ASSET FLOW_____##################
class Test_CreateAssetFlow(unittest.TestCase):

    # CREATE ASSET FLOW assetBody STRING
    def test_createAssetFlow_assetBody_string(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))

    # CREATE ASSET FLOW assetBody CIRCUITFLOW
    def test_createAssetFlow_assetBody_circuitFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        flow = qsoa.CircuitFlow()
        startNode = flow.startNode()
        circuitNode = flow.circuitNode('circuit')
        endNode = flow.endNode()
        flow.linkNodes(startNode, circuitNode)
        flow.linkNodes(circuitNode, endNode)

        assetBody = flow

        assetManagementData = qsoa.createAssetFlow(idSolution_gates, assetName_flow, assetNamespace, assetDescription, assetBody, 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))
    
    # CREATE ASSET FLOW PUBLISH
    def test_createAssetFlow_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        publish = True

        assetManagementData = qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL', publish)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))

    # CREATE ASSET FLOW EXISTING ASSET
    def test_createAssetFlow_existingAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))

    # BAD ARGUMENT idSolution
    def test_createAssetFlow_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlow(99, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetLevel
    def test_createAssetFlow_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetLevel = 'assetLevel'

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, assetLevel)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)
    
    # BAD ARGUMENT publish
    def test_createAssetFlow_badArgument_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        publish = 99

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL', publish)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE idSolution
    def test_createAssetFlow_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlow('idSolution', assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetName
    def test_createAssetFlow_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlow(idSolution_gates, 99, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetNamespace
    def test_createAssetFlow_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, 99, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetDescription
    def test_createAssetFlow_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, 99, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetBody
    def test_createAssetFlow_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, 99, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetLevel
    def test_createAssetFlow_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE publish
    def test_createAssetFlow_badArgumentType_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL', 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_createAssetFlow_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____CREATE ASSET FLOW SYNC_____##################
class Test_CreateAssetFlowSync(unittest.TestCase):

    # CREATE ASSET FLOW SYNC assetBody STRING
    def test_createAssetFlowSync_assetBody_string(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))

    # CREATE ASSET FLOW SYNC assetBody CIRCUITFLOW
    def test_createAssetFlowSync_assetBody_circuitFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        flow = qsoa.CircuitFlow()
        startNode = flow.startNode()
        circuitNode = flow.circuitNode('circuit')
        endNode = flow.endNode()
        flow.linkNodes(startNode, circuitNode)
        flow.linkNodes(circuitNode, endNode)

        assetBody = flow

        assetManagementData = qsoa.createAssetFlowSync(idSolution_gates, assetName_flow, assetNamespace, assetDescription, assetBody, 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))
    
    # CREATE ASSET FLOW SYNC PUBLISH
    def test_createAssetFlowSync_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL', True)

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))

    # CREATE ASSET FLOW SYNC EXISTING ASSET
    def test_createAssetFlowSync_existingAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'FLOW', 'VL'))

    # BAD ARGUMENT idSolution
    def test_createAssetFlowSync_badArgument_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync(99, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT assetLevel
    def test_createAssetFlowSync_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'assetLevel')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)
    
    # BAD ARGUMENT publish
    def test_createAssetFlowSync_badArgument_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL', 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE idSolution
    def test_createAssetFlowSync_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync('idSolution', assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetName
    def test_createAssetFlowSync_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync(idSolution_gates, 99, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetNamespace
    def test_createAssetFlowSync_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, 99, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetDescription
    def test_createAssetFlowSync_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, 99, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetBody
    def test_createAssetFlowSync_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, 99, 'VL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetLevel
    def test_createAssetFlowSync_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE publish
    def test_createAssetFlowSync_badArgumentType_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL', 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_createAssetFlowSync_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.createAssetFlowSync(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____PUBLISH FLOW_____##################
class Test_PublishFlow(unittest.TestCase):

    # PUBLISH FLOW
    def test_publishFlow(self):
        qsoa = QSOAPlatform(configFile=True)
        assetManagementData = qsoa.createAssetFlow(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'VL')
        idFlow = assetManagementData.getIdAsset()

        published = qsoa.publishFlow(idFlow, True)

        self.assertIsInstance(published, bool)
        qsoa.deleteAsset(idFlow, 'FLOW', 'VL')

    # BAD ARGUMENT idFlow
    def test_publishFlow_badArgument_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.publishFlow(99, True)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE idFlow
    def test_publishFlow_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.publishFlow('idFlow', True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE publish
    def test_publishFlow_badArgumentType_publish(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.publishFlow(idFlow_gates, 'publish')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_publishFlow_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.publishFlow(idFlow_gates, True)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____UPDATE ASSET_____##################
class Test_UpdateAsset(unittest.TestCase):

    # UPDATE ASSET
    def test_updateAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        newAssetBody = 'circuit={"cols":[["H"]]}'

        assetManagementData = qsoa.updateAsset(asset, 'newAssetName', 'newAssetNamespace', 'newAssetDescription', newAssetBody, 'GATES', 'VL')

        self.assertEqual(type(assetManagementData).__name__, 'AssetManagementData')

        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        self.assertEqual(asset.getName(), 'newAssetName')
        self.assertEqual(asset.getNamespace(), 'newAssetNamespace')
        self.assertEqual(asset.getDescription(), 'newAssetDescription')
        self.assertEqual(asset.getBody(), newAssetBody)
        self.assertEqual(asset.getType(), 'GATES')
        self.assertEqual(asset.getLevel(), 'VL')
        qsoa.deleteAsset(asset)
    
    # UPDATE ASSET EXISTING NAME
    def test_updateAsset_existingName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData1 = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        assetManagementData2 = qsoa.createAsset(idSolution_gates, assetName_circuit+'2', assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData2.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAsset(asset, assetName_circuit)
            raise Exception
        
        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData1.getIdAsset(), 'CIRCUIT', 'VL'))
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT QUANTITY
    def test_updateAsset_badArgumentQuantity(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        newAssetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=newAssetBody)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetType
    def test_updateAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        newAssetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=newAssetBody, assetType='assetType')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetLevel
    def test_updateAsset_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        newAssetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=newAssetBody, assetType='GATES', assetLevel='assetLevel')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE asset
    def test_updateAsset_badArgumentType_asset(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.updateAsset(99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetName
    def test_updateAsset_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAsset(asset, assetName=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetNamespace
    def test_updateAsset_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAsset(asset, assetNamespace=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetDescription
    def test_updateAsset_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAsset(asset, assetDescription=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetBody
    def test_updateAsset_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAsset(asset, assetBody=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetType
    def test_updateAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        newAssetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=newAssetBody, assetType=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetLevel
    def test_updateAsset_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        newAssetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=newAssetBody, assetType='GATES', assetLevel=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # NOT LOGGED IN
    def test_updateAsset_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        qsoa = QSOAPlatform()

        try:
            qsoa.updateAsset(asset)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')
        
        qsoa = QSOAPlatform(configFile=True)
        qsoa.deleteAsset(asset)


##################_____UPDATE ASSET SYNC_____##################
class Test_UpdateAssetSync(unittest.TestCase):

    # UPDATE ASSET SYNC
    def test_updateAssetSync(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        new_assetBody = 'circuit={"cols":[["H"]]}'

        assetManagementResult = qsoa.updateAssetSync(asset, 'newAssetName', 'newAssetNamespace', 'newAssetDescription', new_assetBody, 'GATES', 'VL')

        self.assertEqual(type(assetManagementResult).__name__, 'AssetManagementResult')

        asset = qsoa.getAsset(assetManagementResult.getIdAsset(), 'CIRCUIT', 'VL')

        self.assertEqual(asset.getName(), 'newAssetName')
        self.assertEqual(asset.getNamespace(), 'newAssetNamespace')
        self.assertEqual(asset.getDescription(), 'newAssetDescription')
        self.assertEqual(asset.getBody(), new_assetBody)
        self.assertEqual(asset.getType(), 'GATES')
        self.assertEqual(asset.getLevel(), 'VL')
        qsoa.deleteAsset(asset)
    
    # UPDATE ASSET SYNC EXISTING NAME
    def test_updateAssetSync_existingName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData1 = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        assetManagementData2 = qsoa.createAsset(idSolution_gates, assetName_circuit+'2', assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData2.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAssetSync(asset, assetName_circuit)
            raise Exception
        
        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData1.getIdAsset(), 'CIRCUIT', 'VL'))
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT QUANTITY
    def test_updateAssetSync_badArgumentQuantity(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        newAssetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAssetSync(asset, assetBody=newAssetBody)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetType
    def test_updateAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        new_assetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType='newAssetType')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetLevel
    def test_updateAsset_badArgument_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        new_assetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType='GATES', assetLevel='newAssetLevel')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE asset
    def test_updateAsset_badArgumentType_asset(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.updateAsset(99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE assetName
    def test_updateAsset_badArgumentType_assetName(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAsset(asset, assetName=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetNamespace
    def test_updateAsset_badArgumentType_assetNamespace(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAsset(asset, assetNamespace=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetDescription
    def test_updateAsset_badArgumentType_assetDescription(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAsset(asset, assetDescription=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetBody
    def test_updateAsset_badArgumentType_assetBody(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.updateAsset(asset, assetBody=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetType
    def test_updateAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        new_assetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetLevel
    def test_updateAsset_badArgumentType_assetLevel(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        new_assetBody = 'circuit={"cols":[["H"]]}'

        try:
            qsoa.updateAsset(asset, assetBody=new_assetBody, assetType='GATES', assetLevel=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # NOT LOGGED IN
    def test_updateAsset_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        qsoa = QSOAPlatform()

        try:
            qsoa.updateAsset(asset)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')
        
        qsoa = QSOAPlatform(configFile=True)
        qsoa.deleteAsset(asset)


##################_____GET ASSET MANAGEMENT RESULT_____##################
class Test_GetAssetManagementResult(unittest.TestCase):

    # GET ASSET MANAGEMENT RESULT
    def test_getAssetManagementResult(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        lifecycleToken = assetManagementData.getLifecycleToken()

        assetManagementResult = qsoa.getAssetManagementResult(lifecycleToken)

        self.assertEqual(type(assetManagementResult).__name__, 'AssetManagementResult')
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL'))

    # BAD ARGUMENT lifecycleToken
    def test_getAssetManagementResult_badArgument_lifecycleToken(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAssetManagementResult('lifecycleToken')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE lifecycleToken
    def test_getAssetManagementResult_badArgumentType_lifecycleToken(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getAssetManagementResult(99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getAssetManagementResult_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getAssetManagementResult('lifecycleToken')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____DELETE ASSET_____##################
class Test_DeleteAsset(unittest.TestCase):

    # DELETE ASSET
    def test_deleteAsset_asset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        assetDeleted = qsoa.deleteAsset(asset)

        self.assertTrue(assetDeleted)

    # DELETE ASSET MANUALLY
    def test_deleteAsset_asset_manually(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        idAsset = asset.getId()

        assetDeleted = qsoa.deleteAsset(idAsset, 'CIRCUIT')

        self.assertTrue(assetDeleted)

    # BAD ARGUMENT idAsset
    def test_deleteAsset_badArgument_idAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.deleteAsset(99, 'CIRCUIT')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT assetType
    def test_deleteAsset_badArgument_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        idAsset = asset.getId()

        try:
            qsoa.deleteAsset(idAsset, 'assetType')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE asset
    def test_deleteAsset_badArgumentType_asset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')

        try:
            qsoa.deleteAsset(99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL'))

    # BAD ARGUMENT TYPE idAsset
    def test_deleteAsset_badArgumentType_idAsset(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        try:
            qsoa.deleteAsset('idAsset', 'CIRCUIT')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # BAD ARGUMENT TYPE assetType
    def test_deleteAsset_badArgumentType_assetType(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        idAsset = asset.getId()

        try:
            qsoa.deleteAsset(idAsset, 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
        qsoa.deleteAsset(asset)

    # NOT LOGGED IN
    def test_deleteAsset_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)

        assetManagementData = qsoa.createAsset(idSolution_gates, assetName_circuit, assetNamespace, assetDescription, assetBody, 'GATES', 'VL')
        asset = qsoa.getAsset(assetManagementData.getIdAsset(), 'CIRCUIT', 'VL')

        qsoa = QSOAPlatform()

        try:
            qsoa.deleteAsset(asset)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')
        
        qsoa = QSOAPlatform(configFile=True)
        qsoa.deleteAsset(asset)


##################_____GET QUANTUM EXECUTION HISTORIC_____##################
class Test_GetQuantumExecutionHistoric(unittest.TestCase):

    # GET QUANTUM EXECUTION HISTORIC
    def test_getQuantumExecutionHistoric(self):
        qsoa = QSOAPlatform(configFile=True)

        quantumExecutionHistoryEntryList = qsoa.getQuantumExecutionHistoric(idSolution_gates)

        self.assertEqual(type(quantumExecutionHistoryEntryList), list)

        firstExecutionHistoryEntry = quantumExecutionHistoryEntryList[0]
        self.assertEqual(type(firstExecutionHistoryEntry).__name__, 'QuantumExecutionHistoryEntry')
    
    # BAD ARGUMENT TYPE idSolution
    def test_getQuantumExecutionHistoric_badArgumentType_idSolution(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionHistoric(idSolution='idSolution')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE idFlow
    def test_getQuantumExecutionHistoric_badArgumentType_idFlow(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionHistoric(idFlow='idFlow')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE idDevice
    def test_getQuantumExecutionHistoric_badArgumentType_idDevice(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionHistoric(idDevice='idDevice')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE dateFrom
    def test_getQuantumExecutionHistoric_badArgumentType_dateFrom(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionHistoric(dateFrom=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE isSimulator
    def test_getQuantumExecutionHistoric_badArgumentType_isSimulator(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionHistoric(isSimulator=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE top
    def test_getQuantumExecutionHistoric_badArgumentType_top(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionHistoric(top='top')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE resultType
    def test_getQuantumExecutionHistoric_badArgumentType_resultType(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionHistoric(resultType=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumExecutionHistoric_notloggedIn(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumExecutionHistoric(idSolution_gates)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


##################_____GET QUANTUM EXECUTION HISTORIC RESULT_____##################
class Test_GetQuantumExecutionHistoricResult(unittest.TestCase):

    # GET QUANTUM EXECUTION HISTORIC RESULT
    def test_getQuantumExecutionHistoricResult(self):
        qsoa = QSOAPlatform(configFile=True)

        quantumExecutionHistoryEntryList = qsoa.getQuantumExecutionHistoric(idSolution_gates)
        idResult = quantumExecutionHistoryEntryList[0].getIdResult()

        quantumExecutionHistoryEntry = qsoa.getQuantumExecutionHistoricResult(idResult)

        self.assertEqual(type(quantumExecutionHistoryEntry).__name__, 'QuantumExecutionHistoryEntry')
    
    # BAD ARGUMENT TYPE idResult
    def test_getQuantumExecutionHistoricResult_badArgumentType_idResult(self):
        qsoa = QSOAPlatform(configFile=True)

        try:
            qsoa.getQuantumExecutionHistoricResult('idResult')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # NOT LOGGED IN
    def test_getQuantumExecutionHistoricResult_notloggedIn(self):
        qsoa = QSOAPlatform(configFile=True)

        quantumExecutionHistoryEntryList = qsoa.getQuantumExecutionHistoric(idSolution_gates)
        idResult = quantumExecutionHistoryEntryList[0].getIdResult()

        qsoa = QSOAPlatform()

        try:
            qsoa.getQuantumExecutionHistoricResult(idResult)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'AuthenticationError')


if __name__ == '__main__':
    unittest.main()