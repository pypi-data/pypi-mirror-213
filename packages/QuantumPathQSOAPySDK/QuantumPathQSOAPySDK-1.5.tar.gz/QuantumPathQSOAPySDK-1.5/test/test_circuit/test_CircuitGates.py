import unittest
from QuantumPathQSOAPySDK import QSOAPlatform

##################_____CIRCUITGATES_____##################
class Test_CircuitGates(unittest.TestCase):

    # CIRCUIT GATES
    def test_CircuitGates(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        self.assertIsInstance(circuit, qsoa.CircuitGates)


##################_____GET CIRCUIT BODY_____##################
class Test_GetCircuitBody(unittest.TestCase):

    # GET CIRCUIT BODY EMPTY
    def test_getCircuitBody_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuitBody = circuit.getCircuitBody()

        self.assertIsInstance(circuitBody, list)
        self.assertEqual(circuitBody, [[]])


##################_____GET PARSED BODY_____##################
class Test_GetParsedBody(unittest.TestCase):

    # GET PARSED BODY EMPTY
    def test_getParsedBody_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        parsedBody = circuit.getParsedBody()

        self.assertIsInstance(parsedBody, str)
        self.assertEqual(parsedBody, 'circuit={"cols": [[]], "init": []}')


##################_____GET QUBIT STATES_____##################
class Test_GetQubitStates(unittest.TestCase):

    # GET QUBIT STATES EMPTY
    def test_getQubitStates_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        qubitStates = circuit.getQubitStates()

        self.assertIsInstance(qubitStates, list)
        self.assertEqual(qubitStates, [])
    
    # GET QUBIT STATES
    def test_getQubitStates(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        qubitStates = circuit.getQubitStates()

        self.assertIsInstance(qubitStates, list)
        self.assertEqual(qubitStates, ['0', '0', '0'])


##################_____GET NUMBER OF QUBITS_____##################
class Test_GetNumberOfQubits(unittest.TestCase):

    # GET NUMBER OF QUBITS EMPTY
    def test_getNumberOfQubits_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        numberOfQubits = circuit.getNumberOfQubits()

        self.assertIsInstance(numberOfQubits, int)
        self.assertEqual(numberOfQubits, 0)
    
    # GET NUMBER OF QUBITS
    def test_getNumberOfQubits(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        numberOfQubits = circuit.getNumberOfQubits()

        self.assertIsInstance(numberOfQubits, int)
        self.assertEqual(numberOfQubits, 3)


##################_____GET DEFAULT QUBIT STATE_____##################
class Test_GetDefaultQubitState(unittest.TestCase):

    # GET DEFAULT QUBIT STATE
    def test_getDefaultQubitState(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        defaultQubitState = circuit.getDefaultQubitState()

        self.assertIsInstance(defaultQubitState, str)
        self.assertEqual(defaultQubitState, '0')


##################_____SET DEFAULT QUBIT STATE_____##################
class Test_SetDefaultQubitState(unittest.TestCase):

    # SET DEFAULT QUBIT STATE
    def test_setDefaultQubitState(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.setDefaultQubitState('1')

        defaultQubitState = circuit.getDefaultQubitState()

        self.assertIsInstance(defaultQubitState, str)
        self.assertEqual(defaultQubitState, '1')

    # SET DEFAULT STATE EXISTING CIRCUIT
    def test_setDefaultQubitState_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)
        circuit.setDefaultQubitState('1')
        circuit.h(2)

        qubitStates = circuit.getQubitStates()

        self.assertIsInstance(qubitStates, list)
        self.assertEqual(qubitStates, ['0', '1', '1'])
    
    # BAD ARGUMENT qubitState
    def test_setDefaultQubitState_badArgument_qubitState(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.setDefaultQubitState('state')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)
    
    # BAD ARGUMENT TYPE qubitState
    def test_setDefaultQubitState_badArgumentType_qubitState(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.setDefaultQubitState(0)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____INITIALIZE QUBIT STATES_____##################
class Test_InitializeQubitStates(unittest.TestCase):

    # INITIALIZE QUBIT STATES
    def test_initializeQubitStates(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        circuit.initializeQubitStates(['1', '1', '1'])

        qubitStates = circuit.getQubitStates()

        self.assertIsInstance(qubitStates, list)
        self.assertEqual(qubitStates, ['1', '1', '1'])

    # BAD ARGUMENT qubitStates
    def test_initializeQubitStates_badArgument_qubitStates(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.initializeQubitStates(['1', '1', '1'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT qubitStates LIST
    def test_initializeQubitStates_badArgument_qubitStates_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.initializeQubitStates(['1', '1', 'state'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE qubitStates
    def test_initializeQubitStates_badArgumentType_qubitStates(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.initializeQubitStates('states')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE qubitStates LIST
    def test_initializeQubitStates_badArgumentType_qubitStates_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        try:
            circuit.initializeQubitStates(['1', '1', 1])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____H_____##################
class Test_H(unittest.TestCase):

    # H position 0
    def test_h_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.h(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['H']])

    # H position 1
    def test_h_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.h(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H']])

    # H EXISTING CIRCUIT position NEW COLUMN
    def test_h_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.h(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['H']])

    # H EXISTING CIRCUIT position SAME COLUMN
    def test_h_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.h(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'H']])

    # H EXISTING CIRCUIT position BETWEEN SWAP
    def test_h_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.h(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'H']])

    # H EXISTING CIRCUIT position UNDER SWAP
    def test_h_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.h(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'H']])

    # H position LIST
    def test_h_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.h([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H'), (1, 'H'), (2, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'H', 'H']])
    
    # H position position LIST EXISTING CIRCUIT
    def test_h_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.h([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H'), (1, 'H'), (2, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'H', 'H'], ['H']])

    # H position position LIST EXISTING CIRCUIT WITH SWAP
    def test_h_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.h([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H'), (1, 'H'), (2, 'H'), (3, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['H', 'H', 'H', 'H']])

    # H position ALL
    def test_h_position_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(1)

        gate = circuit.h()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H'), (1, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'X'], [1, 'H']])
    
    # H position position ALL BETWEEN SWAP
    def test_h_position_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.h()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H'), (1, 'H'), (2, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['H', 'H', 'H']])

    # H add
    def test_h_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.h(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_h_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.h([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_h_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.h('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_h_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.h([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_h_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.h(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____X_____##################
class Test_X(unittest.TestCase):

    # X position 0
    def test_x_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.x(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['X']])

    # X position 1
    def test_x_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.x(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'X']])

    # X EXISTING CIRCUIT position NEW COLUMN
    def test_x_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.x(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['X']])

    # X EXISTING CIRCUIT position SAME COLUMN
    def test_x_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.x(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'X']])

    # X EXISTING CIRCUIT position BETWEEN SWAP
    def test_x_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.x(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'X']])

    # X EXISTING CIRCUIT position UNDER SWAP
    def test_x_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.x(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'X']])

    # X position LIST
    def test_x_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.x([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X'), (1, 'X'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'H', 'X'], [1, 'X']])
    
    # X position position LIST EXISTING CIRCUIT
    def test_x_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.x([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X'), (1, 'X'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'X', 'X'], ['X']])

    # X position position LIST EXISTING CIRCUIT WITH SWAP
    def test_x_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.x([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X'), (1, 'X'), (2, 'X'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['X', 'X', 'X', 'X']])

    # X position ALL
    def test_x_position_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.x()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X'), (1, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'H'], [1, 'X']])

    # X position position ALL BETWEEN SWAP
    def test_x_position_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.x()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X'), (1, 'X'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['X', 'X', 'X']])

    # X add
    def test_x_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.x(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_x_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.x([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_x_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.x('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_x_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.x([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_x_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.x(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____Y_____##################
class Test_Y(unittest.TestCase):

    # Y position 0
    def test_y_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.y(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['Y']])

    # Y position 1
    def test_y_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.y(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'Y']])

    # Y EXISTING CIRCUIT position NEW COLUMN
    def test_y_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.y(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['Y']])

    # Y EXISTING CIRCUIT position SAME COLUMN
    def test_y_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.y(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'Y']])

    # Y EXISTING CIRCUIT position BETWEEN SWAP
    def test_y_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.y(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'Y']])

    # Y EXISTING CIRCUIT position UNDER SWAP
    def test_y_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.y(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'Y']])

    # Y position LIST
    def test_y_position_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.y([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y'), (1, 'Y'), (2, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['Y', 'H', 'Y'], [1, 'Y']])
    
    # Y position position LIST EXISTING CIRCUIT
    def test_y_position_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.y([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y'), (1, 'Y'), (2, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'Y', 'Y'], ['Y']])

    # Y position position LIST EXISTING CIRCUIT WITH SWAP
    def test_y_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.y([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y'), (1, 'Y'), (2, 'Y'), (3, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['Y', 'Y', 'Y', 'Y']])

    # Y position ALL
    def test_y_position_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.y()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y'), (1, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['Y', 'H'], [1, 'Y']])

    # Y position position ALL BETWEEN SWAP
    def test_y_position_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.y()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y'), (1, 'Y'), (2, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['Y', 'Y', 'Y']])

    # Y add
    def test_y_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.y(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_y_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.y([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_y_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.y('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_y_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.y([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_y_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.y(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____Z_____##################
class Test_Z(unittest.TestCase):

    # Z position 0
    def test_z_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.z(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['Z']])

    # Z position 1
    def test_z_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.z(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'Z']])

    # Z EXISTING CIRCUIT position NEW COLUMN
    def test_z_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.z(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['Z']])

    # Z EXISTING CIRCUIT position SAME COLUMN
    def test_z_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.z(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'Z']])

    # Z EXISTING CIRCUIT position BETWEEN SWAP
    def test_z_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.z(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'Z']])

    # Z EXISTING CIRCUIT position UNDER SWAP
    def test_z_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.z(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'Z']])

    # Z position LIST
    def test_z_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.z([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z'), (1, 'Z'), (2, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['Z', 'H', 'Z'], [1, 'Z']])
    
    # Z position position LIST EXISTING CIRCUIT
    def test_z_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.z([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z'), (1, 'Z'), (2, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'Z', 'Z'], ['Z']])

    # Z position position LIST EXISTING CIRCUIT WITH SWAP
    def test_z_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.z([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z'), (1, 'Z'), (2, 'Z'), (3, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['Z', 'Z', 'Z', 'Z']])

    # Z position ALL
    def test_z_position_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.z()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z'), (1, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['Z', 'H'], [1, 'Z']])

    # Z position position ALL BETWEEN SWAP
    def test_z_position_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.z()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z'), (1, 'Z'), (2, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['Z', 'Z', 'Z']])

    # Z add
    def test_z_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.z(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_z_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.z([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_z_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.z('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_z_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.z([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_z_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.z(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____S_____##################
class Test_S(unittest.TestCase):

    # S position 0
    def test_s_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.s(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['S']])

    # S position 1
    def test_s_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.s(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'S']])

    # S EXISTING CIRCUIT position NEW COLUMN
    def test_s_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.s(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['S']])

    # S EXISTING CIRCUIT position SAME COLUMN
    def test_s_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.s(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'S']])

    # S EXISTING CIRCUIT position BETWEEN SWAP
    def test_s_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.s(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'S']])

    # S EXISTING CIRCUIT position UNDER SWAP
    def test_s_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.s(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'S']])

    # S LIST
    def test_s_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.s([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S'), (1, 'S'), (2, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['S', 'H', 'S'], [1, 'S']])
    
    # S position LIST EXISTING CIRCUIT
    def test_s_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.s([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S'), (1, 'S'), (2, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'S', 'S'], ['S']])

    # S position LIST EXISTING CIRCUIT WITH SWAP
    def test_s_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.s([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S'), (1, 'S'), (2, 'S'), (3, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['S', 'S', 'S', 'S']])

    # S ALL
    def test_s_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.s()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S'), (1, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['S', 'H'], [1, 'S']])

    # S position ALL BETWEEN SWAP
    def test_s_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.s()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S'), (1, 'S'), (2, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['S', 'S', 'S']])

    # S add
    def test_s_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.s(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_s_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.s([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_s_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.s('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_s_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.s([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_s_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.s(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_S_____##################
class Test_I_S(unittest.TestCase):

    # I_S
    def test_i_s(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_s(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['I_S']])

    # I_S Q1
    def test_i_s_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_s(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_S']])

    # I_S EXISTING CIRCUIT position NEW COLUMN
    def test_i_s_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_s(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['I_S']])

    # I_S EXISTING CIRCUIT position SAME COLUMN
    def test_i_s_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_s(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'I_S']])

    # I_S EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_s_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_s(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_S']])

    # I_S EXISTING CIRCUIT position UNDER SWAP
    def test_i_s_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_s(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_S']])

    # I_S LIST
    def test_i_s_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_s([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S'), (1, 'I_S'), (2, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['I_S', 'H', 'I_S'], [1, 'I_S']])
    
    # I_S position LIST EXISTING CIRCUIT
    def test_i_s_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.i_s([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S'), (1, 'I_S'), (2, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'I_S', 'I_S'], ['I_S']])

    # I_S position LIST EXISTING CIRCUIT WITH SWAP
    def test_i_s_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_s([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S'), (1, 'I_S'), (2, 'I_S'), (3, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_S', 'I_S', 'I_S', 'I_S']])

    # I_S ALL
    def test_i_s_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_s()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S'), (1, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['I_S', 'H'], [1, 'I_S']])

    # I_S position ALL BETWEEN SWAP
    def test_i_s_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_s()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S'), (1, 'I_S'), (2, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_S', 'I_S', 'I_S']])

    # I_S add
    def test_i_s_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_s(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_s_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_s_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_s_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_i_s_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____SX_____##################
class Test_SX(unittest.TestCase):

    # SX
    def test_sx(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.sx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['SX']])

    # SX Q1
    def test_sx_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.sx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'SX']])

    # SX EXISTING CIRCUIT position NEW COLUMN
    def test_sx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.sx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['SX']])

    # SX EXISTING CIRCUIT position SAME COLUMN
    def test_sx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.sx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'SX']])

    # SX EXISTING CIRCUIT position BETWEEN SWAP
    def test_sx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.sx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'SX']])

    # SX EXISTING CIRCUIT position UNDER SWAP
    def test_sx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.sx(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'SX']])

    # SX LIST
    def test_sx_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.sx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX'), (1, 'SX'), (2, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['SX', 'H', 'SX'], [1, 'SX']])
    
    # SX position LIST EXISTING CIRCUIT
    def test_sx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.sx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX'), (1, 'SX'), (2, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'SX', 'SX'], ['SX']])

    # SX position LIST EXISTING CIRCUIT WITH SWAP
    def test_sx_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.sx([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX'), (1, 'SX'), (2, 'SX'), (3, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['SX', 'SX', 'SX', 'SX']])

    # SX ALL
    def test_sx_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.sx()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX'), (1, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['SX', 'H'], [1, 'SX']])

    # SX position ALL BETWEEN SWAP
    def test_sx_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.sx()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX'), (1, 'SX'), (2, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['SX', 'SX', 'SX']])

    # SX add
    def test_sx_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.sx(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_sx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_sx_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_sx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_sx_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_SX_____##################
class Test_I_SX(unittest.TestCase):

    # I_SX
    def test_i_sx(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['I_SX']])

    # I_SX Q1
    def test_i_sx_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_SX']])

    # I_SX EXISTING CIRCUIT position NEW COLUMN
    def test_i_sx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_sx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['I_SX']])

    # H EXISTING CIRCUIT position SAME COLUMN
    def test_i_sx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_sx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'I_SX']])

    # H EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_sx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_sx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_SX']])

    # H EXISTING CIRCUIT position UNDER SWAP
    def test_i_sx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_sx(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_SX']])

    # I_SX LIST
    def test_i_sx_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_sx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX'), (1, 'I_SX'), (2, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['I_SX', 'H', 'I_SX'], [1, 'I_SX']])
    
    # I_SX position LIST EXISTING CIRCUIT
    def test_i_sx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.i_sx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX'), (1, 'I_SX'), (2, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'I_SX', 'I_SX'], ['I_SX']])

    # I_SX position LIST EXISTING CIRCUIT WITH SWAP
    def test_i_sx_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_sx([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX'), (1, 'I_SX'), (2, 'I_SX'), (3, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_SX', 'I_SX', 'I_SX', 'I_SX']])

    # I_SX ALL
    def test_i_sx_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_sx()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX'), (1, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['I_SX', 'H'], [1, 'I_SX']])

    # I_SX position ALL BETWEEN SWAP
    def test_i_sx_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_sx()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX'), (1, 'I_SX'), (2, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_SX', 'I_SX', 'I_SX']])

    # I_SX add
    def test_i_sx_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sx(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_sx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_sx_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_sx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_i_sx_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____SY_____##################
class Test_SY(unittest.TestCase):

    # SY
    def test_sy(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.sy(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['SY']])

    # SY Q1
    def test_sy_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.sy(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'SY']])

    # SY EXISTING CIRCUIT position NEW COLUMN
    def test_sy_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.sy(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['SY']])

    # SY EXISTING CIRCUIT position SAME COLUMN
    def test_sy_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.sy(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'SY']])

    # SY EXISTING CIRCUIT position BETWEEN SWAP
    def test_sy_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.sy(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'SY']])

    # SY EXISTING CIRCUIT position UNDER SWAP
    def test_sy_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.sy(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'SY']])

    # SY LIST
    def test_sy_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.sy([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY'), (1, 'SY'), (2, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['SY', 'H', 'SY'], [1, 'SY']])
    
    # SY position LIST EXISTING CIRCUIT
    def test_sy_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.sy([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY'), (1, 'SY'), (2, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'SY', 'SY'], ['SY']])

    # SY position LIST EXISTING CIRCUIT WITH SWAP
    def test_sy_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.sy([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY'), (1, 'SY'), (2, 'SY'), (3, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['SY', 'SY', 'SY', 'SY']])

    # SY ALL
    def test_sy_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.sy()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY'), (1, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['SY', 'H'], [1, 'SY']])

    # SY position ALL BETWEEN SWAP
    def test_sy_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.sy()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY'), (1, 'SY'), (2, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['SY', 'SY', 'SY']])

    # SY add
    def test_sy_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.sy(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_sy_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_sy_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_sy_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_sy_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_SY_____##################
class Test_I_SY(unittest.TestCase):

    # I_SY
    def test_i_sy(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sy(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['I_SY']])

    # I_SY Q1
    def test_i_sy_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sy(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_SY']])

    # I_SY EXISTING CIRCUIT position NEW COLUMN
    def test_i_sy_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_sy(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['I_SY']])

    # I_SY EXISTING CIRCUIT position SAME COLUMN
    def test_i_sy_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_sy(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'I_SY']])

    # I_SY EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_sy_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_sy(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_SY']])

    # I_SY EXISTING CIRCUIT position UNDER SWAP
    def test_i_sy_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_sy(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_SY']])

    # I_SY position LIST
    def test_i_sy_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_sy([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY'), (1, 'I_SY'), (2, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['I_SY', 'H', 'I_SY'], [1, 'I_SY']])
    
    # I_SY position position LIST EXISTING CIRCUIT
    def test_i_sy_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.i_sy([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY'), (1, 'I_SY'), (2, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'I_SY', 'I_SY'], ['I_SY']])

    # I_SY position position LIST EXISTING CIRCUIT WITH SWAP
    def test_i_sy_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_sy([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY'), (1, 'I_SY'), (2, 'I_SY'), (3, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_SY', 'I_SY', 'I_SY', 'I_SY']])

    # I_SY position ALL
    def test_i_sy_position_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_sy()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY'), (1, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['I_SY', 'H'], [1, 'I_SY']])

    # I_SY position position ALL BETWEEN SWAP
    def test_i_sy_position_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_sy()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY'), (1, 'I_SY'), (2, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_SY', 'I_SY', 'I_SY']])

    # I_SY add
    def test_i_sy_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sy(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_sy_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_sy_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_sy_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_i_sy_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____T_____##################
class Test_T(unittest.TestCase):

    # T position 0
    def test_t_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.t(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['T']])

    # T position 1
    def test_t_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.t(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'T']])

    # T EXISTING CIRCUIT position NEW COLUMN
    def test_t_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.t(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['T']])

    # T EXISTING CIRCUIT position SAME COLUMN
    def test_t_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.t(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'T']])

    # T EXISTING CIRCUIT position BETWEEN SWAP
    def test_t_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.t(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'T']])

    # T EXISTING CIRCUIT position UNDER SWAP
    def test_t_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.t(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'T']])

    # T position LIST
    def test_t_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.t([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T'), (1, 'T'), (2, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['T', 'H', 'T'], [1, 'T']])
    
    # T position position LIST EXISTING CIRCUIT
    def test_t_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.t([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T'), (1, 'T'), (2, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'T', 'T'], ['T']])

    # T position position LIST EXISTING CIRCUIT WITH SWAP
    def test_t_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.t([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T'), (1, 'T'), (2, 'T'), (3, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['T', 'T', 'T', 'T']])

    # T position ALL
    def test_t_position_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.t()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T'), (1, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['T', 'H'], [1, 'T']])

    # T position position ALL BETWEEN SWAP
    def test_t_position_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.t()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T'), (1, 'T'), (2, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['T', 'T', 'T']])

    # T add
    def test_t_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.t(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT position LIST DUPLICATED
    def test_t_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.t([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_t_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.t('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_t_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.t([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_t_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.t(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_T_____##################
class Test_I_T(unittest.TestCase):

    # I_T position 0
    def test_i_t_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_t(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['I_T']])

    # I_T position 1
    def test_i_t_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_t(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_T']])

    # I_T EXISTING CIRCUIT position NEW COLUMN
    def test_i_t_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_t(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['I_T']])

    # I_T EXISTING CIRCUIT position SAME COLUMN
    def test_i_t_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_t(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'I_T']])

    # I_T EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_t_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_t(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_T']])

    # I_T EXISTING CIRCUIT position UNDER SWAP
    def test_i_t_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_t(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_T']])

    # I_T position LIST
    def test_i_t_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_t([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T'), (1, 'I_T'), (2, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['I_T', 'H', 'I_T'], [1, 'I_T']])
    
    # I_T position position LIST EXISTING CIRCUIT
    def test_i_t_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.i_t([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T'), (1, 'I_T'), (2, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'I_T', 'I_T'], ['I_T']])

    # I_T position position LIST EXISTING CIRCUIT WITH SWAP
    def test_i_t_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_t([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T'), (1, 'I_T'), (2, 'I_T'), (3, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_T', 'I_T', 'I_T', 'I_T']])

    # I_T position ALL
    def test_i_t_position_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_t()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T'), (1, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['I_T', 'H'], [1, 'I_T']])

    # I_T position position ALL BETWEEN SWAP
    def test_i_t_position_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_t()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T'), (1, 'I_T'), (2, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_T', 'I_T', 'I_T']])

    # I_T add
    def test_i_t_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_t(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_t_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_t_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_t_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_i_t_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____TX_____##################
class Test_TX(unittest.TestCase):

    # TX position 0
    def test_tx_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.tx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['TX']])

    # TX position 1
    def test_tx_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.tx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'TX']])

    # TX EXISTING CIRCUIT position NEW COLUMN
    def test_tx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.tx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['TX']])

    # TX EXISTING CIRCUIT position SAME COLUMN
    def test_tx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.tx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'TX']])

    # TX EXISTING CIRCUIT position BETWEEN SWAP
    def test_tx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.tx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'TX']])

    # TX EXISTING CIRCUIT position UNDER SWAP
    def test_tx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.tx(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'TX']])

    # TX LIST
    def test_tx_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.tx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX'), (1, 'TX'), (2, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['TX', 'H', 'TX'], [1, 'TX']])
    
    # TX position LIST EXISTING CIRCUIT
    def test_tx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.tx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX'), (1, 'TX'), (2, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'TX', 'TX'], ['TX']])

    # TX position LIST EXISTING CIRCUIT WITH SWAP
    def test_tx_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.tx([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX'), (1, 'TX'), (2, 'TX'), (3, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['TX', 'TX', 'TX', 'TX']])

    # TX position ALL
    def test_tx_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.tx()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX'), (1, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['TX', 'H'], [1, 'TX']])

    # TX position ALL BETWEEN SWAP
    def test_tx_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.tx()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX'), (1, 'TX'), (2, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['TX', 'TX', 'TX']])

    # TX add
    def test_tx_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.tx(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_tx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_tx_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_tx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_tx_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_TX_____##################
class Test_I_TX(unittest.TestCase):

    # I_TX position 0
    def test_i_tx_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_tx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['I_TX']])

    # I_TX position 1
    def test_i_tx_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_tx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_TX']])

    # I_TX EXISTING CIRCUIT position NEW COLUMN
    def test_i_tx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_tx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['I_TX']])

    # I_TX EXISTING CIRCUIT position SAME COLUMN
    def test_i_tx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_tx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'I_TX']])

    # I_TX EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_tx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_tx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_TX']])

    # I_TX EXISTING CIRCUIT position UNDER SWAP
    def test_i_tx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_tx(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_TX']])

    # I_TX position LIST
    def test_i_tx_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_tx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX'), (1, 'I_TX'), (2, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['I_TX', 'H', 'I_TX'], [1, 'I_TX']])
    
    # I_TX position LIST EXISTING CIRCUIT
    def test_i_tx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.i_tx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX'), (1, 'I_TX'), (2, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'I_TX', 'I_TX'], ['I_TX']])

    # I_TX position LIST EXISTING CIRCUIT WITH SWAP
    def test_i_tx_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_tx([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX'), (1, 'I_TX'), (2, 'I_TX'), (3, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_TX', 'I_TX', 'I_TX', 'I_TX']])

    # I_TX position ALL
    def test_i_tx_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_tx()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX'), (1, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['I_TX', 'H'], [1, 'I_TX']])

    # I_TX position ALL BETWEEN SWAP
    def test_i_tx_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_tx()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX'), (1, 'I_TX'), (2, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_TX', 'I_TX', 'I_TX']])

    # I_TX add
    def test_i_tx_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_tx(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_tx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_tx_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_tx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_i_tx_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____TY_____##################
class Test_TY(unittest.TestCase):

    # TY position 0
    def test_ty_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ty(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['TY']])

    # TY position 1
    def test_ty_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ty(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'TY']])

    # TY EXISTING CIRCUIT position NEW COLUMN
    def test_ty_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ty(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['TY']])

    # TY EXISTING CIRCUIT position SAME COLUMN
    def test_ty_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ty(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'TY']])

    # TY EXISTING CIRCUIT position BETWEEN SWAP
    def test_ty_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.ty(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'TY']])

    # TY EXISTING CIRCUIT position UNDER SWAP
    def test_ty_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.ty(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'TY']])

    # TY position LIST
    def test_ty_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.ty([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY'), (1, 'TY'), (2, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['TY', 'H', 'TY'], [1, 'TY']])
    
    # TY position LIST EXISTING CIRCUIT
    def test_ty_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.ty([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY'), (1, 'TY'), (2, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'TY', 'TY'], ['TY']])

    # TY position LIST EXISTING CIRCUIT WITH SWAP
    def test_ty_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.ty([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY'), (1, 'TY'), (2, 'TY'), (3, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['TY', 'TY', 'TY', 'TY']])

    # TY position ALL
    def test_ty_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.ty()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY'), (1, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['TY', 'H'], [1, 'TY']])

    # TY position ALL BETWEEN SWAP
    def test_ty_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.ty()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY'), (1, 'TY'), (2, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['TY', 'TY', 'TY']])

    # TY add
    def test_ty_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ty(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_ty_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_ty_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_ty_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_ty_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_TY_____##################
class Test_I_TY(unittest.TestCase):

    # I_TY position 0
    def test_i_ty_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_ty(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['I_TY']])

    # I_TY position 1
    def test_i_ty_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_ty(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_TY']])

    # I_TY EXISTING CIRCUIT position NEW COLUMN
    def test_i_ty_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_ty(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['I_TY']])

    # I_TY EXISTING CIRCUIT position SAME COLUMN
    def test_i_ty_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.i_ty(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['H', 'I_TY']])

    # I_TY EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_ty_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_ty(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_TY']])

    # I_TY EXISTING CIRCUIT position UNDER SWAP
    def test_i_ty_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_ty(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_TY']])

    # I_TY position LIST
    def test_i_ty_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_ty([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY'), (1, 'I_TY'), (2, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['I_TY', 'H', 'I_TY'], [1, 'I_TY']])
    
    # I_TY position LIST EXISTING CIRCUIT
    def test_i_ty_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.i_ty([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY'), (1, 'I_TY'), (2, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['X', 'I_TY', 'I_TY'], ['I_TY']])

    # I_TY position LIST EXISTING CIRCUIT WITH SWAP
    def test_i_ty_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_ty([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY'), (1, 'I_TY'), (2, 'I_TY'), (3, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_TY', 'I_TY', 'I_TY', 'I_TY']])

    # I_TY position ALL
    def test_i_ty_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.i_ty()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY'), (1, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['I_TY', 'H'], [1, 'I_TY']])

    # I_TY position ALL BETWEEN SWAP
    def test_i_ty_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_ty()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY'), (1, 'I_TY'), (2, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['I_TY', 'I_TY', 'I_TY']])

    # I_TY add
    def test_i_ty_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.i_ty(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_ty_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_ty_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_ty_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_i_ty_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____P_____##################
class Test_P(unittest.TestCase):

    # P position 0
    def test_p_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.p(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': 'pi'}]])

    # P position 1
    def test_p_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.p(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'P', 'arg': 'pi'}]])

    # P argument INT
    def test_p_argument_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.p(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'P', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'P', 'arg': '2'}]])

    # P argument STRING NUMBER
    def test_p_argument_string_number(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.p(1, '2')

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'P', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'P', 'arg': '2'}]])

    # P argument STRING EXPRESSION
    def test_p_argument_string_expression(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.p(1, 'pi/2')

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'P', 'arg': 'pi/2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'P', 'arg': 'pi/2'}]])

    # P EXISTING CIRCUIT position NEW COLUMN
    def test_p_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.p(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'P', 'arg': 'pi'}]])

    # P EXISTING CIRCUIT position SAME COLUMN
    def test_p_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.p(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['H', {'id': 'P', 'arg': 'pi'}]])

    # P EXISTING CIRCUIT position BETWEEN SWAP
    def test_p_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.p(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'P', 'arg': 'pi'}]])

    # P EXISTING CIRCUIT position UNDER SWAP
    def test_p_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.p(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'P', 'arg': 'pi'}]])

    # P position LIST
    def test_p_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.p([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'P', 'arg': 'pi'}), (1, {'id': 'P', 'arg': 'pi'}), (2, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'P'}, 'H', {'arg': 'pi', 'id': 'P'}], [1, {'arg': 'pi', 'id': 'P'}]])
    
    # P position LIST EXISTING CIRCUIT
    def test_p_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.p([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'P', 'arg': 'pi'}), (1, {'id': 'P', 'arg': 'pi'}), (2, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['X', {'id': 'P', 'arg': 'pi'}, {'id': 'P', 'arg': 'pi'}], [{'id': 'P', 'arg': 'pi'}]])

    # P position LIST EXISTING CIRCUIT WITH SWAP
    def test_p_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.p([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'P', 'arg': 'pi'}), (1, {'id': 'P', 'arg': 'pi'}), (2, {'id': 'P', 'arg': 'pi'}), (3, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'P', 'arg': 'pi'}, {'id': 'P', 'arg': 'pi'}, {'id': 'P', 'arg': 'pi'}, {'id': 'P', 'arg': 'pi'}]])

    # P position ALL
    def test_p_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.p()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'P', 'arg': 'pi'}), (1, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'P'}, 'H'], [1, {'arg': 'pi', 'id': 'P'}]])

    # P position ALL BETWEEN SWAP
    def test_p_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.p()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'P', 'arg': 'pi'}), (1, {'id': 'P', 'arg': 'pi'}), (2, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'P', 'arg': 'pi'}, {'id': 'P', 'arg': 'pi'}, {'id': 'P', 'arg': 'pi'}]])

    # P add
    def test_p_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.p(0, add=False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_p_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.p([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT argument
    def test_p_badArgument_argument(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.p(1, argument='argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_p_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.p('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_p_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.p([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_p_badArgumentType_argument(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.p(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_p_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.p(0, add='add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____RX_____##################
class Test_RX(unittest.TestCase):

    # RX position 0
    def test_rx_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RX', 'arg': 'pi'}]])

    # RX position 1
    def test_rx_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RX', 'arg': 'pi'}]])

    # RX argument INT
    def test_rx_argument_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RX', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RX', 'arg': '2'}]])

    # RX argument STRING NUMBER
    def test_rx_argument_string_number(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(1, '2')

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RX', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RX', 'arg': '2'}]])

    # RX argument STRING EXPRESSION
    def test_rx_argument_string_expression(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(1, 'pi/2')

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RX', 'arg': 'pi/2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RX', 'arg': 'pi/2'}]])

    # RX EXISTING CIRCUIT position NEW COLUMN
    def test_rx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rx(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'RX', 'arg': 'pi'}]])

    # RX EXISTING CIRCUIT position SAME COLUMN
    def test_rx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['H', {'id': 'RX', 'arg': 'pi'}]])

    # RX EXISTING CIRCUIT position BETWEEN SWAP
    def test_rx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.rx(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'RX', 'arg': 'pi'}]])

    # RX EXISTING CIRCUIT position UNDER SWAP
    def test_rx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.rx(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'RX', 'arg': 'pi'}]])

    # RX position LIST
    def test_rx_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.rx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RX', 'arg': 'pi'}), (1, {'id': 'RX', 'arg': 'pi'}), (2, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RX'}, 'H', {'arg': 'pi', 'id': 'RX'}], [1, {'arg': 'pi', 'id': 'RX'}]])
    
    # RX position LIST EXISTING CIRCUIT
    def test_rx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.rx([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RX', 'arg': 'pi'}), (1, {'id': 'RX', 'arg': 'pi'}), (2, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['X', {'id': 'RX', 'arg': 'pi'}, {'id': 'RX', 'arg': 'pi'}], [{'id': 'RX', 'arg': 'pi'}]])

    # RX position LIST EXISTING CIRCUIT WITH SWAP
    def test_rx_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.rx([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RX', 'arg': 'pi'}), (1, {'id': 'RX', 'arg': 'pi'}), (2, {'id': 'RX', 'arg': 'pi'}), (3, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'RX', 'arg': 'pi'}, {'id': 'RX', 'arg': 'pi'}, {'id': 'RX', 'arg': 'pi'}, {'id': 'RX', 'arg': 'pi'}]])

    # RX position ALL
    def test_rx_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.rx()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RX', 'arg': 'pi'}), (1, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RX'}, 'H'], [1, {'arg': 'pi', 'id': 'RX'}]])

    # RX position ALL BETWEEN SWAP
    def test_rx_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.rx() 

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RX', 'arg': 'pi'}), (1, {'id': 'RX', 'arg': 'pi'}), (2, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'RX', 'arg': 'pi'}, {'id': 'RX', 'arg': 'pi'}, {'id': 'RX', 'arg': 'pi'}]])

    # RX add
    def test_rx_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(0, add=False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_rx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT argument
    def test_rx_badArgument_argument(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx(1, argument='argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_rx_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_rx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_rx_badArgumentType_argument(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_rx_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx(0, add='add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____RY_____##################
class Test_RY(unittest.TestCase):

    # RY position 0
    def test_ry_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RY', 'arg': 'pi'}]])

    # RY position 1
    def test_ry_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RY', 'arg': 'pi'}]])

    # RY argument INT
    def test_ry_argument_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RY', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RY', 'arg': '2'}]])

    # RY argument STRING NUMBER
    def test_ry_argument_string_number(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(1, '2')

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RY', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RY', 'arg': '2'}]])

    # P argument STRING EXPRESSION
    def test_ry_argument_string_expression(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(1, 'pi/2')

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RY', 'arg': 'pi/2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RY', 'arg': 'pi/2'}]])

    # RY EXISTING CIRCUIT position NEW COLUMN
    def test_ry_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ry(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'RY', 'arg': 'pi'}]])

    # RY EXISTING CIRCUIT position SAME COLUMN
    def test_ry_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ry(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['H', {'id': 'RY', 'arg': 'pi'}]])

    # RY EXISTING CIRCUIT position BETWEEN SWAP
    def test_ry_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.ry(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'RY', 'arg': 'pi'}]])

    # RY EXISTING CIRCUIT position UNDER SWAP
    def test_ry_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.ry(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'RY', 'arg': 'pi'}]])

    # RY position LIST
    def test_ry_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.ry([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RY', 'arg': 'pi'}), (1, {'id': 'RY', 'arg': 'pi'}), (2, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RY'}, 'H', {'arg': 'pi', 'id': 'RY'}], [1, {'arg': 'pi', 'id': 'RY'}]])
    
    # RY position LIST EXISTING CIRCUIT
    def test_ry_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.ry([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RY', 'arg': 'pi'}), (1, {'id': 'RY', 'arg': 'pi'}), (2, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['X', {'id': 'RY', 'arg': 'pi'}, {'id': 'RY', 'arg': 'pi'}], [{'id': 'RY', 'arg': 'pi'}]])

    # RY position LIST EXISTING CIRCUIT WITH SWAP
    def test_ry_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.ry([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RY', 'arg': 'pi'}), (1, {'id': 'RY', 'arg': 'pi'}), (2, {'id': 'RY', 'arg': 'pi'}), (3, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'RY', 'arg': 'pi'}, {'id': 'RY', 'arg': 'pi'}, {'id': 'RY', 'arg': 'pi'}, {'id': 'RY', 'arg': 'pi'}]])

    # RY position ALL
    def test_ry_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.ry()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RY', 'arg': 'pi'}), (1, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RY'}, 'H'], [1, {'arg': 'pi', 'id': 'RY'}]])

    # RY position ALL BETWEEN SWAP
    def test_ry_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.ry() 

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RY', 'arg': 'pi'}), (1, {'id': 'RY', 'arg': 'pi'}), (2, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'RY', 'arg': 'pi'}, {'id': 'RY', 'arg': 'pi'}, {'id': 'RY', 'arg': 'pi'}]])

    # RY add
    def test_ry_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(0, add=False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_ry_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT argument
    def test_ry_badArgument_argument(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry(1, argument='argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_ry_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_ry_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_ry_badArgumentType_argument(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_ry_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry(0, add='add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____RZ_____##################
class Test_RZ(unittest.TestCase):

    # RZ position_0
    def test_rz_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RZ', 'arg': 'pi'}]])

    # RZ position 1
    def test_rz_position_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RZ', 'arg': 'pi'}]])

    # RZ argument INT
    def test_rz_argument_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RZ', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RZ', 'arg': '2'}]])

    # RZ argument STRING NUMBER
    def test_rz_argument_string_number(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(1, '2')

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RZ', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RZ', 'arg': '2'}]])

    # P argument STRING EXPRESSION
    def test_rz_argument_string_expression(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(1, 'pi/2')

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RZ', 'arg': 'pi/2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RZ', 'arg': 'pi/2'}]])

    # RZ EXISTING CIRCUIT position NEW COLUMN
    def test_rz_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rz(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'RZ', 'arg': 'pi'}]])

    # RZ EXISTING CIRCUIT position SAME COLUMN
    def test_rz_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rz(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['H', {'id': 'RZ', 'arg': 'pi'}]])

    # RZ EXISTING CIRCUIT position BETWEEN SWAP
    def test_rz_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.rz(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'RZ', 'arg': 'pi'}]])

    # RZ EXISTING CIRCUIT position UNDER SWAP
    def test_rz_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.rz(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'RZ', 'arg': 'pi'}]])

    # RZ position LIST
    def test_rz_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.rz([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RZ', 'arg': 'pi'}), (1, {'id': 'RZ', 'arg': 'pi'}), (2, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RZ'}, 'H', {'arg': 'pi', 'id': 'RZ'}], [1, {'arg': 'pi', 'id': 'RZ'}]])
    
    # RZ position LIST EXISTING CIRCUIT
    def test_rz_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.rz([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RZ', 'arg': 'pi'}), (1, {'id': 'RZ', 'arg': 'pi'}), (2, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['X', {'id': 'RZ', 'arg': 'pi'}, {'id': 'RZ', 'arg': 'pi'}], [{'id': 'RZ', 'arg': 'pi'}]])

    # RZ position LIST EXISTING CIRCUIT WITH SWAP
    def test_rz_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.rz([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RZ', 'arg': 'pi'}), (1, {'id': 'RZ', 'arg': 'pi'}), (2, {'id': 'RZ', 'arg': 'pi'}), (3, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'RZ', 'arg': 'pi'}, {'id': 'RZ', 'arg': 'pi'}, {'id': 'RZ', 'arg': 'pi'}, {'id': 'RZ', 'arg': 'pi'}]])

    # RZ position ALL
    def test_rz_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.rz()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RZ', 'arg': 'pi'}), (1, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RZ'}, 'H'], [1, {'arg': 'pi', 'id': 'RZ'}]])

    # RZ position ALL BETWEEN SWAP
    def test_rz_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.rz() 

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RZ', 'arg': 'pi'}), (1, {'id': 'RZ', 'arg': 'pi'}), (2, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'RZ', 'arg': 'pi'}, {'id': 'RZ', 'arg': 'pi'}, {'id': 'RZ', 'arg': 'pi'}]])

    # RZ add
    def test_rz_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(0, add=False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_rz_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT argument
    def test_rz_badArgument_argument(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz(1, argument='argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_rz_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_rz_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_rz_badArgumentType_argument(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_rz_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz(0, add='add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____SWAP_____##################
class Test_Swap(unittest.TestCase):

    # SWAP position 0, 1
    def test_swap_position_0_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.swap(0, 1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Swap'), (1, 'Swap')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap']])

    # SWAP position 0, 2
    def test_swap_position_0_2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.swap(0, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Swap'), (2, 'Swap')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap']])

    # SWAP position 1, 2
    def test_swap_position_position_1_2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.swap(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Swap'), (2, 'Swap')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'Swap', 'Swap']])

    # SWAP EXISTING CIRCUIT position NEW COLUMN
    def test_swap_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.swap(0, 1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Swap'), (1, 'Swap')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['Swap', 'Swap']])

    # SWAP EXISTING CIRCUIT position SAME COLUMN
    def test_swap_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.swap(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Swap'), (2, 'Swap')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'Swap', 'Swap']])

    # SWAP EXISTING CIRCUIT position BETWEEN SWAP
    def test_swap_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 3)

        gate = circuit.swap(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Swap'), (2, 'Swap')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 1, 'Swap'], [1, 'Swap', 'Swap']])

    # SWAP EXISTING CIRCUIT position UNDER SWAP
    def test_swap_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.swap(2, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'Swap'), (3, 'Swap')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'Swap', 'Swap']])

    # SWAP add
    def test_swap_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.swap(1, 3, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Swap'), (3, 'Swap')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE position1
    def test_swap_badArgumentType_position1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap('position', 3)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_swap_badArgumentType_position2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap(1, 'position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_swap_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap(1, 3, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CH_____##################
class Test_CH(unittest.TestCase):

    # CH position 0, 1
    def test_ch_0_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ch(0, 1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'H']])

    # CH position 0, 2
    def test_ch_position_0_2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ch(0, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (2, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 1, 'H']])

    # CH position 1, 2
    def test_ch_position_position_1_2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ch(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'H']])

    # CH EXISTING CIRCUIT position NEW COLUMN
    def test_ch_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ch(0, 1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['CTRL', 'H']])

    # CH EXISTING CIRCUIT position SAME COLUMN
    def test_ch_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ch(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'H']])

    # CH EXISTING CIRCUIT position BETWEEN SWAP
    def test_ch_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 3)

        gate = circuit.ch(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 1, 'Swap'], [1, 'CTRL', 'H']])

    # CH EXISTING CIRCUIT position UNDER SWAP
    def test_ch_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.ch(2, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'CTRL'), (3, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'CTRL', 'H']])

    # CH add
    def test_ch_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ch(1, 3, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (3, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE position1
    def test_ch_badArgumentType_position1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch('position', 3)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_ch_badArgumentType_position2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch(1, 'position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_ch_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch(1, 3, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CX_____##################
class Test_CX(unittest.TestCase):

    # CX position 0, 1
    def test_cx_position_0_1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.cx(0, 1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # CX position 0, 2
    def test_cx_position_0_2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.cx(0, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 1, 'X']])

    # CX position 1, 2
    def test_cx_position_position_1_2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.cx(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'X']])

    # CX EXISTING CIRCUIT position NEW COLUMN
    def test_cx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.cx(0, 1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['CTRL', 'X']])

    # CX EXISTING CIRCUIT position SAME COLUMN
    def test_cx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.cx(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'X']])

    # CX EXISTING CIRCUIT position BETWEEN SWAP
    def test_cx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 3)

        gate = circuit.cx(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 1, 'Swap'], [1, 'CTRL', 'X']])

    # CX EXISTING CIRCUIT position UNDER SWAP
    def test_cx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.cx(2, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'CTRL', 'X']])

    # CX add
    def test_cx_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.cx(1, 3, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE position1
    def test_cx_badArgumentType_position1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx('position', 3)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_cx_badArgumentType_position2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx(1, 'position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_cx_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx(1, 3, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CCX_____##################
class Test_CCX(unittest.TestCase):

    # CCX position 0, 1, 2
    def test_ccx_position_0_1_2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(0, 1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'CTRL'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 'X']])

    # CCX position 0, 1, 3
    def test_ccx_position_0_1_3(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(0, 1, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 1, 'X']])

    # CCX position 1, 2, 3
    def test_ccx_position_position_1_2_3(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(1, 2, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'CTRL', 'X']])

    # CCX EXISTING CIRCUIT position NEW COLUMN
    def test_ccx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ccx(0, 1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'CTRL'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['CTRL', 'CTRL', 'X']])

    # CCX EXISTING CIRCUIT position SAME COLUMN
    def test_ccx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ccx(1, 2, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'CTRL', 'X']])

    # CCX EXISTING CIRCUIT position BETWEEN SWAP
    def test_ccx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 4)

        gate = circuit.ccx(1, 2, 3)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 1, 1, 'Swap'], [1, 'CTRL', 'CTRL', 'X']])

    # CCX EXISTING CIRCUIT position UNDER SWAP
    def test_ccx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.ccx(2, 3, 4)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'CTRL'), (3, 'CTRL'), (4, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'CTRL', 'CTRL', 'X']])

    # CCX add
    def test_ccx_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(1, 2, 3, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'CTRL'), (2, 'CTRL'), (3, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE position1
    def test_ccx_badArgumentType_position1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx('position', 2, 3)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_ccx_badArgumentType_position2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(1, 'position', 3)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position3
    def test_ccx_badArgumentType_position3(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(1, 2, 'position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_ccx_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(1, 2, 3, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____MEASURE_____##################
class Test_Measure(unittest.TestCase):

    # MEASURE position 0
    def test_measure_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.measure(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Measure']])

    # MEASURE EXISTING CIRCUIT position NEW COLUMN
    def test_measure_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.measure(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['Measure']])

    # MEASURE EXISTING CIRCUIT position SAME COLUMN
    def test_measure_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.measure(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'Measure']])

    # MEASURE EXISTING CIRCUIT position BETWEEN SWAP
    def test_measure_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.measure(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'Measure']])

    # MEASURE EXISTING CIRCUIT position UNDER SWAP
    def test_measure_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.measure(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'Measure']])

    # MEASURE position LIST
    def test_measure_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.measure([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure'), (2, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['Measure', 'Measure', 'Measure']])
    
    # MEASURE position LIST EXISTING CIRCUIT
    def test_measure_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.measure([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure'), (2, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['X'], ['Measure', 'Measure', 'Measure']])

    # MEASURE position LIST EXISTING CIRCUIT WITH SWAP
    def test_measure_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.measure([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure'), (2, 'Measure'), (3, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['Measure', 'Measure', 'Measure', 'Measure']])

    # MEASURE position ALL
    def test_measure_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.measure()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['Measure', 'Measure']])

    # MEASURE position ALL BETWEEN SWAP
    def test_measure_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.measure()

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Measure'), (1, 'Measure'), (2, 'Measure')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['Measure', 'Measure', 'Measure']])
    
    # BAD ARGUMENT position LIST DUPLICATED
    def test_measure_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_measure_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_measure_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____BARRIER_____##################
class Test_Barrier(unittest.TestCase):

    # BARRIER position 0
    def test_barrier_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.barrier(0)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['SPACER']])

    # BARRIER EXISTING CIRCUIT position NEW COLUMN
    def test_barrier_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.barrier(0)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['SPACER']])

    # BARRIER EXISTING CIRCUIT position SAME COLUMN
    def test_barrier_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.barrier(1)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['H', 'SPACER']])

    # BARRIER EXISTING CIRCUIT position BETWEEN SWAP
    def test_barrier_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.barrier(1)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'SPACER']])

    # BARRIER EXISTING CIRCUIT position UNDER SWAP
    def test_barrier_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.barrier(2)

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'SPACER']])

    # BARRIER position LIST
    def test_barrier_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.barrier([0, 1, 2])

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['SPACER', 'H', 'SPACER'], [1, 'SPACER']])
    
    # BARRIER position LIST EXISTING CIRCUIT
    def test_barrier_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.barrier([0, 1, 2])

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['X', 'SPACER', 'SPACER'], ['SPACER']])

    # BARRIER position LIST EXISTING CIRCUIT WITH SWAP
    def test_barrier_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.barrier([0, 1, 2, 3])

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['SPACER', 'SPACER', 'SPACER', 'SPACER']])

    # BARRIER position ALL
    def test_barrier_position_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.barrier()

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['SPACER', 'SPACER']])

    # BARRIER position ALL BETWEEN SWAP
    def test_barrier_position_all_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.barrier()

        self.assertIsNone(gate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['SPACER', 'SPACER', 'SPACER']])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_barrier_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_barrier_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_barrier_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____BEGIN REPEAT_____##################
class Test_BeginRepeat(unittest.TestCase):

    # BEGIN REPEAT position 0
    def test_beginRepeat_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.beginRepeat(0, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[{'arg': '2', 'id': 'BEGIN_R'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position NEW COLUMN
    def test_beginRepeat_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.beginRepeat(0, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position SAME COLUMN
    def test_beginRepeat_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.beginRepeat(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, {'arg': '2', 'id': 'BEGIN_R'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position BETWEEN SWAP
    def test_beginRepeat_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.beginRepeat(1, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position UNDER SWAP
    def test_beginRepeat_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.beginRepeat(2, 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT position LIST
    def test_beginRepeat_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.beginRepeat([0, 1], 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'}), (1, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], [{'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT position LIST EXISTING CIRCUIT
    def test_beginRepeat_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.beginRepeat([0, 1, 2], 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'}), (1, {'id': 'BEGIN_R', 'arg': '2'}), (2, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['X'], [{'arg': '2', 'id': 'BEGIN_R'}, {'arg': '2', 'id': 'BEGIN_R'}, {'arg': '2', 'id': 'BEGIN_R'}]])

    # BEGIN REPEAT position LIST EXISTING CIRCUIT WITH SWAP
    def test_beginRepeat_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.beginRepeat([0, 1, 2, 3], 2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'BEGIN_R', 'arg': '2'}), (1, {'id': 'BEGIN_R', 'arg': '2'}), (2, {'id': 'BEGIN_R', 'arg': '2'}), (3, {'id': 'BEGIN_R', 'arg': '2'})])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [{'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_beginRepeat_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat([0, 0], 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_beginRepeat_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat('position', 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_beginRepeat_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat([0, 'position'], 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE repetitions
    def test_beginRepeat_badArgumentType_argument(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat(0, 'repetitions')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____END REPEAT_____##################
class Test_EndRepeat(unittest.TestCase):

    # END REPEAT position 0
    def test_endRepeat_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.endRepeat(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['END_R']])

    # END REPEAT EXISTING CIRCUIT position NEW COLUMN
    def test_endRepeat_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.endRepeat(0)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['END_R']])

    # END REPEAT EXISTING CIRCUIT position SAME COLUMN
    def test_endRepeat_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.endRepeat(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'END_R']])

    # END REPEAT EXISTING CIRCUIT position BETWEEN SWAP
    def test_endRepeat_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.endRepeat(1)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'END_R']])

    # END REPEAT EXISTING CIRCUIT position UNDER SWAP
    def test_endRepeat_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.endRepeat(2)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'END_R']])

    # END REPEAT position LIST
    def test_endRepeat_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.endRepeat([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R'), (1, 'END_R'), (2, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['END_R', 'END_R', 'END_R']])

    # END REPEAT position LIST EXISTING CIRCUIT
    def test_endRepeat_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.endRepeat([0, 1, 2])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R'), (1, 'END_R'), (2, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['X'], ['END_R', 'END_R', 'END_R']])

    # END REPEAT position LIST EXISTING CIRCUIT WITH SWAP
    def test_endRepeat_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.endRepeat([0, 1, 2, 3])

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'END_R'), (1, 'END_R'), (2, 'END_R'), (3, 'END_R')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['END_R', 'END_R', 'END_R', 'END_R']])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_endRepeat_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_endRepeat_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_endRepeat_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CONTROL_____##################
class Test_Control(unittest.TestCase):

    # CONTROL position 0
    def test_control_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        cx = circuit.control(0, circuit.x(1, False))
        circuit.addCreatedGate(cx)

        self.assertEqual(cx, [(1, 'X'), (0, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # BAD ARGUMENT TYPE position
    def test_control_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            cx = circuit.control('position', circuit.h(0, False))
            circuit.addCreatedGate(cx)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE circuit
    def test_control_badArgumentType_circuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.control(0, 'circuit')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ADD CREATED GATE_____##################
class Test_AddCreatedGate(unittest.TestCase):

    # ADD CREATED GATE position 0
    def test_addCreatedGate_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        cx = circuit.control(0, circuit.x(1, False))
        circuit.addCreatedGate(cx)

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # BAD ARGUMENT TYPE gate
    def test_addCreatedGate_badArgumentType_gate(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.addCreatedGate('gate')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____MULTI CONTROL GATE_____##################
class Test_MCG(unittest.TestCase):

    # MCG position 0
    def test_mcg_position_0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.mcg(0, circuit.x(1, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'X'), (0, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # MCG EXISTING CIRCUIT position NEW COLUMN
    def test_mcg_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.mcg(0, circuit.x(1, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'X'), (0, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['CTRL', 'X']])

    # MCG EXISTING CIRCUIT position SAME COLUMN
    def test_mcg_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.mcg(1, circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'X']])

    # MCG EXISTING CIRCUIT position BETWEEN SWAP
    def test_mcg_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 3)

        gate = circuit.mcg(1, circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 1, 'Swap'], [1, 'CTRL', 'X']])

    # MCG EXISTING CIRCUIT position UNDER SWAP
    def test_mcg_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.mcg(2, circuit.x(3, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (2, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'CTRL', 'X']])

    # MCG position LIST
    def test_mcg_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.mcg([0, 2], circuit.x(3, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (0, 'CTRL'), (2, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['CTRL', 1, 'CTRL', 'X']])

    # MCG position LIST EXISTING CIRCUIT
    def test_mcg_position_list_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.mcg([0, 1], circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (0, 'CTRL'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['X'], ['CTRL', 'CTRL', 'X']])

    # MCG position LIST EXISTING CIRCUIT WITH SWAP
    def test_mcg_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.mcg([0, 1], circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (0, 'CTRL'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['CTRL', 'CTRL', 'X']])

    # MCG add
    def test_mcg_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.mcg([0, 2], circuit.x(3, False), False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (0, 'CTRL'), (2, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position LIST DUPLICATED
    def test_mcg_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 0], circuit.x(3))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT circuit
    def test_mcg_badArgument_circuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        gate = circuit.mcg(1, circuit.x(3))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (1, 'CTRL')])
        self.assertNotEqual(circuit.getCircuitBody(), [[1, 'CTRL', 1, 'X']])

    # BAD ARGUMENT TYPE position
    def test_mcg_badArgumentType_position(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg('position', circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_mcg_badArgumentType_position_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 'position'], circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_mcg_badArgumentType_add(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 2], circuit.x(3, False), 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()