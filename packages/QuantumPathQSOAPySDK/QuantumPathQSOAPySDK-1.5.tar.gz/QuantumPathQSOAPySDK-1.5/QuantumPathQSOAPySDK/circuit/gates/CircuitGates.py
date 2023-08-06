from ...utils.checker import checkInputTypes, checkValues, checkMathExpression, checkDifferentPosition

class CircuitGates:

    # CONSTRUCTOR
    def __init__(self):
        """
        CircuitGates object constructor.

        Prerequisites
        ----------
        None.

        Output
        ----------
        CircuitGates obj
        """

        self.__circuitBody = [[]]
        self.__qubitStates = []
        self.__numerOfQubits = 0
        self.__defaultQubitState = '0'

        self.__circuitVLStructure = {
            'cols': self.__circuitBody,
            'init': self.__qubitStates
        }

    # GETTERS
    def getCircuitBody(self) -> list:
        """
        Get Circuit Body.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        list
        """

        return self.__circuitBody

    def getParsedBody(self) -> str:
        """
        Get Circuit Body VL.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        str
        """

        parsedtBody = 'circuit=' +  str(self.__circuitVLStructure).replace("'", '"')

        return parsedtBody

    def getQubitStates(self) -> list:
        """
        Get Circuit Qubit states.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        list
        """

        return self.__qubitStates

    def getNumberOfQubits(self) -> int:
        """
        Get number of qubits used in circuit.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        int
        """

        return self.__numerOfQubits

    def getDefaultQubitState(self) -> str:
        """
        Get Default Qubit state.

        Prerequisites
        ----------
        - Created circuit.
        
        Output
        ----------
        str
        """
        
        return self.__defaultQubitState

    # SETTERS
    def setDefaultQubitState(self, qubitState: str) -> str:
        """
        Set Default Qubit state.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        qubitState : str
            Set default qubit state. It can be 0, 1, +, -, i or -i.

        Output
        ----------
        str
        """
        checkInputTypes(
            ('qubitState', qubitState, (str,))
        )
        checkValues(('qubitStates', qubitState, ['0', '1', '+', '-', 'i', '-i']))

        self.__defaultQubitState = qubitState # set new default qubit state

        return self.__qubitStates


    # INTERN FUNCTIONS
    def __addSimpleGate(self, position, gate, circuitBody):
        numColumn = len(circuitBody) - 1 # column index
        lastColumn = -1 # last column with gate

        # SEARCH LAST COLUMN TO ADD
        while numColumn >= 0: # while there are columns

            if 'CTRL' in circuitBody[numColumn] or 'Swap' in circuitBody[numColumn]: # column have a multiple gate
                break

            elif len(circuitBody[numColumn]) - 1 < position: # column is smaller than the gate position
                lastColumn = numColumn # column available to add the gate
            
            else: # column is greater than the gate position

                if circuitBody[numColumn][position] == 1: # position is 1
                    lastColumn = numColumn # column available to add the gate
                
                else: # column have a gate, so is not available to add the gate
                    break

            numColumn -= 1 # check previous column

        # ADD GATE
        if lastColumn != -1: # add the gate in an existing column

            if len(circuitBody[lastColumn]) - 1 < position: # column is smaller than the gate position

                while len(circuitBody[lastColumn]) != position: # fill with 1 the positions until the gate position
                    circuitBody[lastColumn].append(1)
                
                circuitBody[lastColumn].append(gate) # add the gate
            
            else: # column is larger than the gate position
                circuitBody[lastColumn][position] = gate # replace 1 by the gate
        
        else: # add a new column
            circuitBody.append([])

            while len(circuitBody[lastColumn]) != position: # fill with 1 the positions until the gate position
                circuitBody[-1].append(1)
                
            circuitBody[-1].append(gate) # add the gate

    def __addMultipleGate(self, positions, circuitBody):
        positions = sorted(positions)

        # SEARCH LAST COLUMN TO ADD
        if circuitBody[0] == []: # circuit is empty
            lastColumn = 0

        else: # if circuit is not empty
            lastColumn = -1
            circuitBody.append([])
        
        # ADD GATE
        for position in positions:

            while len(circuitBody[lastColumn]) != position[0]: # fill with 1 the positions until the gate position
                circuitBody[lastColumn].append(1)
            
            circuitBody[lastColumn].append(position[1]) # add the gate

    def __definePositions(self, position, gate: str, circuitBody: list) -> list:
        positions = list()

        if isinstance(position, int): # gate in one position
            positions.append((position, gate))
        
        elif isinstance(position, list): # gate in multiple positions
            for i in position:
                positions.append((i, gate)) # add all controls
        
        elif position is None:
            lenCircuitBody = list()

            for column in circuitBody:
                lenCircuitBody.append(len(column))

            times = max(lenCircuitBody)

            for i in range(times):
                positions.append((i, gate))
            
        return positions

    def __updateQubits(self):
        new_numerOfQubits = max(len(x) for x in self.__circuitBody) # new number of qubits

        if new_numerOfQubits > self.__numerOfQubits:
            while len(self.__qubitStates) < new_numerOfQubits:
                self.__qubitStates.append(self.__defaultQubitState) # add new qubit states
        
        self.__numerOfQubits = new_numerOfQubits
    

    # METHODS
    def initializeQubitStates(self, qubitStates: list):
        """
        Initialize Qubit states.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        qbitStates : list
            List of strings setting up the qubit states. It must be equal than number of qubits. There can be 0, 1, +, -, i or -i.
        """
        checkInputTypes(
            ('qubitStates', qubitStates, (list,))
        )

        for qubitState in qubitStates:
            checkInputTypes(('qubitStates', qubitState, (str,)))
            checkValues(('qubitStates', qubitState, ['0', '1', '+', '-', 'i', '-i']))
        
        if len(qubitStates) != self.__numerOfQubits:
            raise ValueError(f'Incorrect number of qubit states. Input states are {len(qubitStates)} and should be {self.__numerOfQubits}')

        self.__qubitStates = qubitStates

    def h(self, position: int = None, add: bool = True) -> list: # hadamard gate
        """
        Add Hadamard gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'H'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
            
        self.__updateQubits()
        
        return positions

    def x(self, position: int = None, add: bool = True) -> list: # not gate
        """
        Add Pauli X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )
        
        gateSymbol = 'X'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions
    
    def y(self, position: int = None, add: bool = True) -> list: # pauli y gate
        """
        Add Pauli Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'Y'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def z(self, position: int = None, add: bool = True) -> list: # pauli z gate
        """
        Add Pauli Z gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'Z'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def s(self, position: int = None, add: bool = True) -> list: # square root of z, s gate
        """
        Add Square root of Z, S gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'S'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def i_s(self, position: int = None, add: bool = True) -> list: # Adjoint square root z gate
        """
        Add Adjoint square root Z gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'I_S'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def sx(self, position: int = None, add: bool = True) -> list: # square root of not gate
        """
        Add Square root of X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'SX'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def i_sx(self, position: int = None, add: bool = True) -> list: # adjoint square root X gate
        """
        Add Adjoint square root X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'I_SX'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def sy(self, position: int = None, add: bool = True) -> list: # square root of y gate
        """
        Add Square root of Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'SY'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def i_sy(self, position: int = None, add: bool = True) -> list: # adjoint square root y gate
        """
        Add Adjoint square root Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'I_SY'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def t(self, position: int = None, add: bool = True) -> list: # four root of z, t gate
        """
        Add Four root of Z, T gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'T'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def i_t(self, position: int = None, add: bool = True) -> list: # adjoint four root z gate
        """
        Add Adjoint four root Z gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'I_T'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def tx(self, position: int = None, add: bool = True) -> list: # four root of x gate
        """
        Add four root of X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'TX'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def i_tx(self, position: int = None, add: bool = True) -> list: # adjoint four root X gate
        """
        Add Adjoint four root X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'I_TX'
        
        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def ty(self, position: int = None, add: bool = True) -> list: # four root of y gate
        """
        Add four root of Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'TY'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def i_ty(self, position: int = None, add: bool = True) -> list: # adjoint four root y gate
        """
        Add Adjoint four root Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        gateSymbol = 'I_TY'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def p(self, position: int = None, argument = 'pi', add: bool = True) -> list: # phase gate
        """
        Add Phase gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        argument: string
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('argument', argument, (str, int)),
            ('add', add, (bool,))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        gateSymbol = {'id': 'P', 'arg': str(argument)}

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def rx(self, position: int = None, argument = 'pi', add: bool = True) -> list: # rotation x gate
        """
        Add Rotation X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        argument: string
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('argument', argument, (str, int)),
            ('add', add, (bool,))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        gateSymbol = {'id': 'RX', 'arg': str(argument)}

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def ry(self, position: int = None, argument = 'pi', add: bool = True) -> list: # rotation y gate
        """
        Add Rotation Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        argument: string
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('argument', argument, (str, int)),
            ('add', add, (bool,))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        gateSymbol = {'id': 'RY', 'arg': str(argument)}

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def rz(self, position: int = None, argument = 'pi', add: bool = True) -> list: # rotation z gate
        """
        Add Rotation Z gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. Argument can also be a list of positions.
        argument: string
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('argument', argument, (str, int)),
            ('add', add, (bool,))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        gateSymbol = {'id': 'RZ', 'arg': str(argument)}

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        if add:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def swap(self, position1: int, position2: int, add: bool = True) -> list: # swap gate
        """
        Add Rotation Swap gates.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the swap.
        position2 : int
            Mandatory argument. Second qubit position to add the swap.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('add', add, (bool,)),
        )

        positions = [
            (position1, 'Swap'),
            (position2, 'Swap')
        ]

        if add:
            self.__addMultipleGate(positions, self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def ch(self, position1: int, position2: int, add: bool = True) -> list: # control hadamard gate
        """
        Add Rotation Control Hadamard gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the control.
        position2 : int
            Mandatory argument. Second qubit position to add the hadamard gate.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('add', add, (bool,)),
        )

        positions = [
            (position1, 'CTRL'),
            (position2, 'H')
        ]

        if add:
            self.__addMultipleGate(positions, self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def cx(self, position1: int, position2: int, add: bool = True) -> list: # control not gate
        """
        Add Control X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the control.
        position2 : int
            Mandatory argument. Second qubit position to add the X gate.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('add', add, (bool,)),
        )

        positions = [
            (position1, 'CTRL'),
            (position2, 'X')
        ]

        if add:
            self.__addMultipleGate(positions, self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def ccx(self, position1: int, position2: int, position3: int, add = True) -> list: # toffoli gate
        """
        Add Toffoli gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the control.
        position2 : int
            Mandatory argument. Second qubit position to add the control.
        position3 : int
            Mandatory argument. Third qubit position to add the X gate.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('position3', position3, (int,)),
            ('add', add, (bool,)),
        )

        positions = [
            (position1, 'CTRL'),
            (position2, 'CTRL'),
            (position3, 'X')
        ]

        if add:
            self.__addMultipleGate(positions, self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return positions

    def measure(self, position: int = None) -> list: # measure
        """
        Add Measure.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the measurement. In the case that the position is not indicated, the measurement will be added in all qubits. It can also be a list of positions.
        
        Output
        ----------
        list
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)

        gateSymbol = 'Measure'
        
        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        self.__addMultipleGate(positions, self.__circuitBody) # add to circuit

        self.__updateQubits()
        
        return positions

    def barrier(self, position: int = None): # barrier
        """
        Add Barrier.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the barrier. In the case that the position is not indicated, the barrier will be added in all qubits. It can also be a list of positions.
        """
        if position:
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                for p in position:
                    checkInputTypes(('position', p, (int,)))
                checkDifferentPosition(position)

        gateSymbol = 'SPACER'

        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure
        
        if position is None:
            self.__addMultipleGate(positions, self.__circuitBody) # add to circuit
        
        else:
            for gate in positions: # to all gates
                self.__addSimpleGate(gate[0], gate[1], self.__circuitBody) # add to circuit
        
        self.__updateQubits()

    def beginRepeat(self, position: int, repetitions: int) -> list: # begin repeat
        """
        Add Begin Repeat.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Qubit position to add the begin repetition. It can also be a list of positions.
        repetitions: int
            Number of repetitions.
        
        Output
        ----------
        list
        """
        checkInputTypes(
            ('position', position, (int, list))
        )
        if isinstance(position, list):
            for p in position:
                checkInputTypes(('position', p, (int,)))
            checkDifferentPosition(position)
        checkInputTypes(
            ('repetitions', repetitions, (int,))
        )

        gateSymbol = {'id': 'BEGIN_R', 'arg': str(repetitions)}
        
        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        self.__addMultipleGate(positions, self.__circuitBody) # add to circuit

        self.__updateQubits()
        
        return positions

    def endRepeat(self, position: int) -> list: # begin repeat
        """
        Add End Repeat.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Qubit position to add the end repetition. It can also be a list of positions.
        
        Output
        ----------
        list
        """
        checkInputTypes(
            ('position', position, (int, list))
        )
        if isinstance(position, list):
            for p in position:
                checkInputTypes(('position', p, (int,)))
            checkDifferentPosition(position)

        gateSymbol = 'END_R'
        
        positions = self.__definePositions(position, gateSymbol, self.__circuitBody) # get gate position structure

        self.__addMultipleGate(positions, self.__circuitBody) # add to circuit

        self.__updateQubits()
        
        return positions

    def control(self, position: int, circuit: list) -> list: # control
        """
        Add Control.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Mandatory argument. Qubit position to add the control. It can also be a list of positions.
        circuit : list
            Gate or set of elements to add a control.
        
        Output
        ----------
        list
        """
        checkInputTypes(
            ('position', position, (int, list)),
            ('circuit', circuit, (list,))
        )
        if isinstance(position, list):
            for p in position:
                checkInputTypes(('position', p, (int,)))
            checkDifferentPosition(position)

        correctPosition = True

        for gate in circuit:
            if position in gate:
                correctPosition = False
                break

        if correctPosition:
            circuit.append((position, 'CTRL'))

        self.__updateQubits()

        return circuit

    def addCreatedGate(self, gate: list): # add created gate
        """
        Add Created gate.

        Prerequisites
        ----------
        - Created circuit.
        - Created gate.

        Parameters
        ----------
        gate : list
            Created gate to add to the circuit.
        """
        checkInputTypes(
            ('gate', gate, (list,))
        )

        self.__addMultipleGate(gate, self.__circuitBody) # add to circuit

        self.__updateQubits()

    def mcg(self, position: int, circuit: list, add: bool = True) -> list: # multi control gate
        """
        Add Multi Control gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Qubit position or list of positions to add the control. It can also be a list of positions.
        circuit : list
            Gate or set of elements to add a control.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        checkInputTypes(
            ('position', position, (int, list)),
            ('circuit', circuit, (list,)),
            ('add', add, (bool,)),
        )
        if isinstance(position, list):
            for p in position:
                checkInputTypes(('position', p, (int,)))
            checkDifferentPosition(position)
        
        gateSymbol = 'CTRL'

        if isinstance(position, int): # one postion
            circuit.append((position, gateSymbol))

        elif isinstance(position, list): # multiple positions
            for i in position:
                circuit.append((i, gateSymbol)) # add all controls

        if add:
            self.__addMultipleGate(circuit, self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return circuit