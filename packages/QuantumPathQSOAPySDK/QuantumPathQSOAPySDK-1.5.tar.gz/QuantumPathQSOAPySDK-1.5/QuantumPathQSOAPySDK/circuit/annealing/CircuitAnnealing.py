from ...utils.checker import (checkInputTypes)

class CircuitAnnealing:
    from .components import (
        Parameter,
        AuxData,
        Class,
        Variable,
        Rule,
        OffsetExp,
        LinearExp,
        QuadraticExp,
        SquaredExp,
        SummatoryExp
    )
    
    # CONSTRUCTOR
    def __init__(self):
        """
        CircuitAnnealing object constructor.

        Prerequisites
        ----------
        None.

        Output
        ----------
        CircuitAnnealing obj
        """

        self.__parameters = []
        self.__auxData = []
        self.__classes = []
        self.__variables = []
        self.__rules = []

        self.__circuitBody = {
            'Parameters': self.__parameters,
            'AuxData': self.__auxData,
            'Classes': self.__classes,
            'Variables': self.__variables,
            'Rules': self.__rules
        }
    

    # GETTERS
    def getCircuitBody(self) -> dict:
        """
        Get Circuit Body.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        dict
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

        parsedtBody = str(self.__circuitBody).replace("'", '"').replace('"True"', 'true').replace('"False"', 'false')

        return parsedtBody

    def getParameters(self) -> list:
        """
        Get Circuit Parameters.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        list
        """

        return self.__parameters

    def getAuxData(self) -> list:
        """
        Get Circuit Auxiliary data.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        list
        """

        return self.__auxData

    def getClasses(self) -> list:
        """
        Get Circuit Classes.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        list
        """

        return self.__classes

    def getVariables(self) -> list:
        """
        Get Circuit Variables.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        list
        """

        return self.__variables
    
    def getRules(self) -> list:
        """
        Get Circuit Rules.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        list
        """

        return self.__rules


    # METHODS
    def addParameter(self, parameter):
        """
        Add Circuit Parameter.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        parameter : Parameter obj | list
            Circuit Parameter object or list of Parameter objects.
        
        Output
        ----------
        Parameter obj | Parameter obj list
        """
        def appendParameter(parameter):
            self.__parameters.append({
                'uiID': parameter.getUiID(),
                'Name': parameter.getName(),
                'Value': parameter.getValue()
            })

        checkInputTypes(
            ('parameter', parameter, (self.Parameter, list))
        )
        if isinstance(parameter, list):
            if not parameter:
                raise ValueError('List of parameters should not be empty')

            for p in parameter:
                checkInputTypes(('parameter', p, (self.Parameter,)))

            for p in parameter:
                appendParameter(p)
        
        else:
            appendParameter(parameter)
        
        return parameter

    def addAuxData(self, auxData):
        """
        Add Circuit Auxiliary Data.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        auxData : AuxData obj | list
            Circuit Auxiliary Data object or list of Auxiliary Data objects.
        
        Output
        ----------
        AuxData obj | AuxData obj list
        """
        def appendAuxData(auxData):
            self.__auxData.append({
                'uiID': auxData.getUiID(),
                'Name': auxData.getName(),
                'Value': auxData.getValue()
            })

        checkInputTypes(
            ('auxData', auxData, (self.AuxData, list))
        )
        if isinstance(auxData, list):
            if not auxData:
                raise ValueError('List of auxiliary data should not be empty')

            for a in auxData:
                checkInputTypes(('auxData', a, (self.AuxData,)))

            for a in auxData:
                appendAuxData(a)
        
        else:
            appendAuxData(auxData)
        
        return auxData

    def addClass(self, cls):
        """
        Add Circuit Class.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        cls : Class obj | list
            Circuit Class object or list of Class objects.
        
        Output
        ----------
        Class obj | Class obj list
        """
        def appendClass(cls):
            self.__classes.append({
                'Properties': cls.getProperties(),
                'uiID': cls.getUiID(),
                'Name': cls.getName(),
                'NumberOfVars': cls.getNumberOfVars(),
                'Description': cls.getDescription()
            })

        checkInputTypes(
            ('circuitClass', cls, (self.Class, list))
        )
        if isinstance(cls, list):
            if not cls:
                raise ValueError('List of classes should not be empty')

            for c in cls:
                checkInputTypes(('cls', c, (self.Class,)))

            for c in cls:
                appendClass(c)
        
        else:
            appendClass(cls)

        return cls

    def addVariable(self, variable):
        """
        Add Circuit Variable.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        variable : Variable obj | list
            Circuit Variable object or list of Variable objects.
        
        Output
        ----------
        Variable obj | Variable obj list
        """
        def appendVariable(variable):
            self.__variables.append({
                'Classes': variable.getClasses(),
                'uiID': variable.getUiID(),
                'Name': variable.getName(),
                'Description': variable.getDescription()
            })

        checkInputTypes(
            ('variable', variable, (self.Variable, list))
        )
        if isinstance(variable, list):
            if not variable:
                raise ValueError('List of variables should not be empty')

            for v in variable:
                checkInputTypes(('variable', v, (self.Variable,)))

            for v in variable:
                appendVariable(v)
        
        else:
            appendVariable(variable)
        
        return variable

    def addRule(self, rule):
        """
        Add Circuit Rule.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        rule : Rule obj | list
            Circuit Rule object or list of Rule objects.
        
        Output
        ----------
        Rule obj | Rule obj list
        """
        def appendRule(rule):
            self.__rules.append({
                'Expressions': rule.getExpressions(),
                'uiID': rule.getUiID(),
                'Name': rule.getName(),
                'Lambda': rule.getLambda(),
                'Description': rule.getDescription(),
                'Disabled': rule.getDisabled()
            })

        checkInputTypes(
            ('rule', rule, (self.Rule, list))
        )
        if isinstance(rule, list):
            if not rule:
                raise ValueError('List of rules should not be empty')

            for r in rule:
                checkInputTypes(('rule', r, (self.Rule,)))

            for r in rule:
                appendRule(r)
        
        else:
            appendRule(rule)
        
        return rule