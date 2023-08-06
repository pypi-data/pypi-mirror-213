import unittest
import time
from QuantumPathQSOAPySDK import QSOAPlatform

# GATES
idSolution_gates = 10651
idDevice_gates = 2
idFlow_gates = 1798
executionToken_gates = '60f4c608-8308-4ad8-b2a3-c3beb8a2c125'

# ANNEALING
idSolution_annealing = 10652
idFlow_annealing = 1799
executionToken_annealing = '08b571e0-61f1-47cb-b1a8-d01967cc2a99'

# ASSET
idAsset = 26475
assetName_circuit = 'test_circuit'
assetName_flow = 'test_flow'
assetDescription = 'assetDescription'
assetNamespace = 'TestPySDK'
assetBody = 'circuit={"cols":[["H"],["CTRL","X"],["Measure","Measure"]]}'

def waitForApplicationResponse(qsoa: QSOAPlatform, application):
    execution = qsoa.getQuantumExecutionResponse(application)

    while execution.getExitCode() == 'WAIT':
        time.sleep(1)
        execution = qsoa.getQuantumExecutionResponse(application)


##################_____QSOAPLATFORM_____##################
class Test_QSOAPlatform(unittest.TestCase):

    # NOT AUTHENTICATE
    def test_QSOAPlatform_notAuthenticate(self):
        qsoa = QSOAPlatform()

        authenticated = qsoa.echostatus()

        self.assertFalse(authenticated)

    '''
    INTRODUCE MANUALLY USERNAME AND PASSWORD
    '''
    # AUTHENTICATE MANUALLY
    # def test_QSOAPlatform_manually(self):
    #     username = 'username'
    #     password = 'password' # password in SHA-256

    #     qsoa = QSOAPlatform(username, password)

    #     authenticated = qsoa.echostatus()

    #     self.assertTrue(authenticated)

    '''
    CREATE .QPATH CONFIG FILE
    '''
    # AUTHENTICATE CONFIG FILE
    # def test_QSOAPlatform_configFile(self):
    #     qsoa = QSOAPlatform(configFile=True)

    #     authenticated = qsoa.authenticateEx()

    #     self.assertTrue(authenticated)

    # AUTHENTICATE USER MANUALLY BAD CREDENTIALS
    def test_QSOAPlatform_manually_badArgument_username_password(self):
        username = 'username'
        password = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8' # password encrypted in SHA-256

        try:
            QSOAPlatform(username, password)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE username
    def test_QSOAPlatform_badArgumentType_username(self):
        username = 99
        password = 'password'

        try:
            QSOAPlatform(username, password)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE password
    def test_QSOAPlatform_badArgumentType_password(self):
        username = 'username'
        password = 99

        try:
            QSOAPlatform(username, password)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE configFile
    def test_QSOAPlatform_badArgumentType_configFile(self):
        try:
            QSOAPlatform(configFile=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()