import unittest
from QuantumPathQSOAPySDK import QSOAPlatform

def removeUiID(result):
    def removeUiIDDict(dictionary):
        if 'uiID' in dictionary:
            del dictionary['uiID']
        for value in dictionary.values():
            if isinstance(value, dict):
                removeUiID([value])
            elif isinstance(value, list):
                for element in value:
                    if isinstance(element, dict):
                        removeUiID([element])

    if isinstance(result, list):
        for dictionary in result:
            removeUiIDDict(dictionary)
    elif isinstance(result, dict):
        removeUiIDDict(result)


##################_____CIRCUITANNEALING_____##################
class Test_CircuitAnnealing(unittest.TestCase):

    # CIRCUIT ANNEALING
    def test_CircuitAnnealing(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        self.assertIsInstance(circuit, qsoa.CircuitAnnealing)


##################_____GET CIRCUIT BODY_____##################
class Test_GetCircuitBody(unittest.TestCase):

    # GET CIRCUIT BODY
    def test_getCircuitBody(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        circuitBody = circuit.getCircuitBody()

        self.assertIsInstance(circuitBody, dict)
        self.assertEqual(circuitBody, {'Parameters': [], 'AuxData': [], 'Classes': [], 'Variables': [], 'Rules': []})


##################_____GET PARSED BODY_____##################
class Test_GetParsedBody(unittest.TestCase):

    # GET PARSED BODY EMPTY
    def test_getParsedBody_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        parsedBody = circuit.getParsedBody()

        self.assertIsInstance(parsedBody, str)
        self.assertEqual(parsedBody, '{"Parameters": [], "AuxData": [], "Classes": [], "Variables": [], "Rules": []}')


##################_____GET PARAMETERS_____##################
class Test_GetParameters(unittest.TestCase):

    # GET PARAMETERS EMPTY
    def test_getParameters_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        parameters = circuit.getParameters()

        self.assertIsInstance(parameters, list)
        self.assertEqual(parameters, [])

    # GET PARAMETERS
    def test_getParameters(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        circuit.addParameter(circuit.Parameter('Parameter', 1))

        parameters = circuit.getParameters()
        removeUiID(parameters) # remove random uiID to validate behaviour

        self.assertIsInstance(parameters, list)
        self.assertIsInstance(parameters[0], dict)
        self.assertEqual(parameters, [{'Name': 'Parameter', 'Value': '1'}])


##################_____GET AUXILIARY DATA_____##################
class Test_GetAuxData(unittest.TestCase):

    # GET PARAMETERS EMPTY
    def test_getAuxData_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        auxData = circuit.getAuxData()

        self.assertIsInstance(auxData, list)
        self.assertEqual(auxData, [])

    # GET AUXILIARY DATA
    def test_getAuxData(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        circuit.addAuxData(circuit.AuxData('AuxData', 1))

        auxData = circuit.getAuxData()
        removeUiID(auxData) # remove random uiID to validate behaviour

        self.assertIsInstance(auxData, list)
        self.assertIsInstance(auxData[0], dict)
        self.assertEqual(auxData, [{'Name': 'AuxData', 'Value': '1'}])


##################_____GET CLASSES_____##################
class Test_GetClasses(unittest.TestCase):

    # GET CLASSES EMPTY
    def test_getClasses_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        classes = circuit.getClasses()

        self.assertIsInstance(classes, list)
        self.assertEqual(classes, [])

    # GET CLASSES
    def test_getClasses(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        circuit.addClass(circuit.Class('Class', 1))

        classes = circuit.getClasses()
        removeUiID(classes) # remove random uiID to validate behaviour

        self.assertIsInstance(classes, list)
        self.assertIsInstance(classes[0], dict)
        self.assertEqual(classes, [{'Description': '', 'Name': 'Class', 'NumberOfVars': '1', 'Properties': []}])


##################_____GET VARIABLES_____##################
class Test_GetVariables(unittest.TestCase):

    # GET VARIABLES EMPTY
    def test_getVariables_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        variables = circuit.getVariables()

        self.assertIsInstance(variables, list)
        self.assertEqual(variables, [])

    # GET VARIABLES
    def test_getVariables(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 1)
        circuit.addVariable(circuit.Variable('Variable', cls))

        variables = circuit.getVariables()
        removeUiID(variables) # remove random uiID to validate behaviour # remove random uiID to validate behaviour

        self.assertIsInstance(variables, list)
        self.assertEqual(variables, [{'Classes': [cls.getUiID()], 'Name': 'Variable', 'Description': ''}])


##################_____GET RULES_____##################
class Test_GetRules(unittest.TestCase):

    # GET RULES EMPTY
    def test_getRules_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        rules = circuit.getRules()

        self.assertIsInstance(rules, list)
        self.assertEqual(rules, [])

    # GET RULES
    def test_getRules(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)
        circuit.addRule(rule)

        rules = circuit.getRules()
        removeUiID(rules) # remove random uiID to validate behaviour

        self.assertIsInstance(rules, list)
        self.assertIsInstance(rules[0], dict)
        self.assertEqual(rules, [{'Expressions': [], 'Name': 'Rule', 'Lambda': '1', 'Description': '', 'Disabled': 'False'}])


##################_____PARAMETER_____##################
class Test_Parameter(unittest.TestCase):

    # PARAMETER value INT
    def test_Parameter_value_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        parameter = circuit.Parameter('Parameter', 1)

        self.assertIsInstance(parameter, circuit.Parameter)
        self.assertEqual(parameter.getName(), 'Parameter')
        self.assertEqual(parameter.getValue(), '1')

    # PARAMETER value STRING EXPRESSION
    def test_Parameter_value_string_expression(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        parameter = circuit.Parameter('Parameter', 'pi/2')

        self.assertIsInstance(parameter, circuit.Parameter)
        self.assertEqual(parameter.getName(), 'Parameter')
        self.assertEqual(parameter.getValue(), 'pi/2')

    # BAD ARGUMENT value
    def test_Parameter_badArgument_value(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Parameter('Parameter', 'value')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE name
    def test_Parameter_badArgumentType_name(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Parameter(1, 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE value
    def test_Parameter_badArgumentType_value(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Parameter('Parameter', True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____AUXDATA_____##################
class Test_AuxData(unittest.TestCase):

    # AUXDATA value INT
    def test_AuxData_value_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        auxData = circuit.AuxData('AuxData', 1)

        self.assertIsInstance(auxData, circuit.AuxData)
        self.assertEqual(auxData.getName(), 'AuxData')
        self.assertEqual(auxData.getValue(), '1')

    # AUXDATA value LIST
    def test_AuxData_value_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        auxData = circuit.AuxData('AuxData', [1, 1])

        self.assertIsInstance(auxData, circuit.AuxData)
        self.assertEqual(auxData.getName(), 'AuxData')
        self.assertEqual(auxData.getValue(), '[1, 1]')

    # BAD ARGUMENT value LIST
    def test_AuxData_badArgument_value_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.AuxData('AuxData', [])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE name
    def test_AuxData_badArgumentType_name(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.AuxData(99, 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE value STRING
    def test_AuxData_badArgumentType_value_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.AuxData('AuxData', 'value')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE value LIST
    def test_AuxData_badArgumentType_value_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.AuxData('AuxData', [1, 'value'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CLASS_____##################
class Test_Class(unittest.TestCase):

    # CLASS numberOfVars INT
    def test_Class_numberOfVars_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        cls = circuit.Class('Class', 2)

        self.assertIsInstance(cls, circuit.Class)
        self.assertEqual(cls.getName(), 'Class')
        self.assertEqual(cls.getNumberOfVars(), '2')
        self.assertEqual(cls.getDescription(), '')
        self.assertEqual(cls.getProperties(), [])

    # CLASS numberOfVars PARAMETER
    def test_Class_numberOfVars_Parameter(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        parameter = circuit.Parameter('Parameter', 2)

        cls = circuit.Class('Class', parameter)

        self.assertIsInstance(cls, circuit.Class)
        self.assertEqual(cls.getName(), 'Class')
        self.assertEqual(cls.getNumberOfVars(), '2')
        self.assertEqual(cls.getDescription(), '')
        self.assertEqual(cls.getProperties(), [])

    # CLASS description
    def test_Class_description(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        cls = circuit.Class('Class', 2, description='description')

        self.assertIsInstance(cls, circuit.Class)
        self.assertEqual(cls.getName(), 'Class')
        self.assertEqual(cls.getNumberOfVars(), '2')
        self.assertEqual(cls.getDescription(), 'description')
        self.assertEqual(cls.getProperties(), [])

    # BAD ARGUMENT TYPE name
    def test_Class_badArgumentType_name(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Class(99, 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE numberOfVars
    def test_Class_badArgumentType_numberOfVars(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Class('Class', 'numberOfVars')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE description
    def test_Class_badArgumentType_description(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Class('Class', 2, 99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CLASS ADD PROPERTY_____##################
class Test_Class_AddProperty(unittest.TestCase):

    # ADD PROPERTY CLASS numberOfVars INT
    def test_Class_addProperty_Class_numberOfVars_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        cls = circuit.Class('Class', 2)
        cls.addProperty('Property', [1, 2])
        circuit.addClass(cls)
        
        properties = circuit.getClasses()[0]['Properties']
        removeUiID(properties) # remove random uiID to validate behaviour

        self.assertIsInstance(properties, list)
        self.assertEqual(properties, [{'Name': 'Property', 'Values': ['1', '2']}])

    # ADD PROPERTY CLASS numberOfVars PARAMETER
    def test_Class_addProperty_Class_numberOfVars_Parameter(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        cls = circuit.Class('Class', circuit.Parameter('Parameter', 2))
        cls.addProperty('Property', [1, 2])
        circuit.addClass(cls)
        
        properties = circuit.getClasses()[0]['Properties']
        removeUiID(properties) # remove random uiID to validate behaviour

        self.assertIsInstance(properties, list)
        self.assertEqual(properties, [{'Name': 'Property', 'Values': ['1', '2']}])

    # BAD ARGUMENT value
    def test_Class_addProperty_badArgument_value(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 2)

        try:
            cls.addProperty('Property', [1, 2, 3])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE name
    def test_Class_addProperty_badArgumentType_name(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 2)

        try:
            cls.addProperty(99, [1, 2])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE value STRING
    def test_Class_addProperty_badArgumentType_value_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 2)

        try:
            cls.addProperty('Property', 'value')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
    # BAD ARGUMENT TYPE value LIST
    def test_Class_addProperty_badArgumentType_value_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 2)

        try:
            cls.addProperty('Property', [1, 'value'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____VARIABLE_____##################
class Test_Variable(unittest.TestCase):

    # VARIABLE classes CLASS
    def test_Variable_classes_Class(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        cls = circuit.Class('Class', 1)

        variable = circuit.Variable('Variable', cls)
        
        self.assertIsInstance(variable, circuit.Variable)
        self.assertEqual(variable.getName(), 'Variable')
        self.assertEqual(variable.getClasses(), [cls.getUiID()])
        self.assertEqual(variable.getDescription(), '')

    # VARIABLE classes LIST
    def test_Variable_classes_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        cls1 = circuit.Class('Class', 1)
        cls2 = circuit.Class('Class2', 2)

        variable = circuit.Variable('Variable', [cls1, cls2])
        
        self.assertIsInstance(variable, circuit.Variable)
        self.assertEqual(variable.getName(), 'Variable')
        self.assertEqual(variable.getClasses(), [cls1.getUiID(), cls2.getUiID()])
        self.assertEqual(variable.getDescription(), '')

    # VARIABLE description
    def test_Variable_description(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 1)

        variable = circuit.Variable('Variable', cls, description='description')
        
        self.assertIsInstance(variable, circuit.Variable)
        self.assertEqual(variable.getName(), 'Variable')
        self.assertEqual(variable.getClasses(), [cls.getUiID()])
        self.assertEqual(variable.getDescription(), 'description')

    # BAD ARGUMENT classes LIST
    def test_Variable_badArgument_classes_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Variable('Variable', [])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE name
    def test_Variable_badArgumentType_name(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 1)

        try:
            circuit.Variable(99, cls)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE classes STRING
    def test_Variable_badArgumentType_classes_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Variable('Variable', 'classes')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE classes LIST
    def test_Variable_badArgumentType_classes_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 1)

        try:
            circuit.Variable('Variable', [cls, 'cls'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE description
    def test_Variable_badArgumentType_description(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 1)

        try:
            circuit.Variable('Variable', cls, 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____RULE_____##################
class Test_Rule(unittest.TestCase):

    # RULE lambdaValue INT
    def test_Rule_lambdaValue_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        rule = circuit.Rule('Rule', 1)
        
        self.assertIsInstance(rule, circuit.Rule)
        self.assertEqual(rule.getName(), 'Rule')
        self.assertEqual(rule.getLambda(), '1')
        self.assertEqual(rule.getDescription(), '')
        self.assertEqual(rule.getDisabled(), 'False')
        self.assertEqual(rule.getExpressions(), [])

    # RULE lambdaValue STRING
    def test_Rule_lambdaValue_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        rule = circuit.Rule('Rule', 'pi/2')
        
        self.assertIsInstance(rule, circuit.Rule)
        self.assertEqual(rule.getName(), 'Rule')
        self.assertEqual(rule.getLambda(), 'pi/2')
        self.assertEqual(rule.getDescription(), '')
        self.assertEqual(rule.getDisabled(), 'False')
        self.assertEqual(rule.getExpressions(), [])

    # RULE description
    def test_Rule_description(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        rule = circuit.Rule('Rule', 1, description='description')
        
        self.assertIsInstance(rule, circuit.Rule)
        self.assertEqual(rule.getName(), 'Rule')
        self.assertEqual(rule.getLambda(), '1')
        self.assertEqual(rule.getDescription(), 'description')
        self.assertEqual(rule.getDisabled(), 'False')
        self.assertEqual(rule.getExpressions(), [])

    # RULE disabled
    def test_Rule_disabled(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        rule = circuit.Rule('Rule', 1, disabled=True)
        
        self.assertIsInstance(rule, circuit.Rule)
        self.assertEqual(rule.getName(), 'Rule')
        self.assertEqual(rule.getLambda(), '1')
        self.assertEqual(rule.getDescription(), '')
        self.assertEqual(rule.getDisabled(), 'True')
        self.assertEqual(rule.getExpressions(), [])

    # BAD ARGUMENT lambdaValue STRING
    def test_Rule_badArgument_lambdaValue_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Rule('Rule', 'lambdaValue')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE name
    def test_Rule_badArgumentType_name(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Rule(1, 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE lambdaValue
    def test_Rule_badArgumentType_lambdaValue(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Rule('Rule', True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE description
    def test_Rule_badArgumentType_description(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Rule('Rule', 1, description=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE disabled
    def test_Rule_badArgumentType_disabled(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.Rule('Rule', 1, disabled='disabled')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____OFFSETEXP_____##################
class Test_OffsetExp(unittest.TestCase):

    # OFFSET EXPRESSION offset INT
    def test_OffsetExp_offset_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        offsetExp = circuit.OffsetExp(1)
        
        self.assertIsInstance(offsetExp, circuit.OffsetExp)
        self.assertEqual(offsetExp.getExpType(), 'OFFSET')
        self.assertEqual(offsetExp.getCoefficient(), '')
        self.assertEqual(offsetExp.getOffset(), '1')
        self.assertEqual(offsetExp.getFrom(), '')
        self.assertEqual(offsetExp.getTo(), '')
        self.assertEqual(offsetExp.getIterator(), '')
        self.assertEqual(offsetExp.getTerm1(), {})
        self.assertEqual(offsetExp.getTerm2(), {})
        self.assertEqual(offsetExp.getChilds(), [])

    # OFFSET EXPRESSION offset STRING
    def test_OffsetExp_offset_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        offsetExp = circuit.OffsetExp('offset')
        
        self.assertIsInstance(offsetExp, circuit.OffsetExp)
        self.assertEqual(offsetExp.getExpType(), 'OFFSET')
        self.assertEqual(offsetExp.getCoefficient(), '')
        self.assertEqual(offsetExp.getOffset(), 'offset')
        self.assertEqual(offsetExp.getFrom(), '')
        self.assertEqual(offsetExp.getTo(), '')
        self.assertEqual(offsetExp.getIterator(), '')
        self.assertEqual(offsetExp.getTerm1(), {})
        self.assertEqual(offsetExp.getTerm2(), {})
        self.assertEqual(offsetExp.getChilds(), [])

    # BAD ARGUMENT TYPE offset
    def test_OffsetExp_badArgumentType_offset(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.OffsetExp(True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____LINEAREXP_____##################
class Test_LinearExp(unittest.TestCase):

    # LINEAR EXPRESSION variable[1] INT
    def test_LinearExp_variable1_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable = circuit.Variable('Variable', cls:=circuit.Class('Class', 1))
        
        linearExp = circuit.LinearExp((variable, 1))
        
        self.assertIsInstance(linearExp, circuit.LinearExp)
        self.assertEqual(linearExp.getExpType(), 'LINEAR')
        self.assertEqual(linearExp.getCoefficient(), '')
        self.assertEqual(linearExp.getOffset(), '')
        self.assertEqual(linearExp.getFrom(), '')
        self.assertEqual(linearExp.getTo(), '')
        self.assertEqual(linearExp.getIterator(), '')
        term1 = linearExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()})
        self.assertEqual(linearExp.getTerm2(), {})
        self.assertEqual(linearExp.getChilds(), [])

    # LINEAR EXPRESSION variable[1] STRING
    def test_LinearExp_variable1_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable = circuit.Variable('Variable', cls:=circuit.Class('Class', 1))

        linearExp = circuit.LinearExp((variable, 'value'))
        
        self.assertIsInstance(linearExp, circuit.LinearExp)
        self.assertEqual(linearExp.getExpType(), 'LINEAR')
        self.assertEqual(linearExp.getCoefficient(), '')
        self.assertEqual(linearExp.getOffset(), '')
        self.assertEqual(linearExp.getFrom(), '')
        self.assertEqual(linearExp.getTo(), '')
        self.assertEqual(linearExp.getIterator(), '')
        term1 = linearExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': 'value', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()})
        self.assertEqual(linearExp.getTerm2(), {})
        self.assertEqual(linearExp.getChilds(), [])

    # LINEAR EXPRESSION variable[1] LIST INT, STRING
    def test_LinearExp_variable1_list_int_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable = circuit.Variable('Variable', cls:=[circuit.Class('Class', 1), circuit.Class('Class', 1)])

        linearExp = circuit.LinearExp((variable, [1, 'value']))
        
        self.assertIsInstance(linearExp, circuit.LinearExp)
        self.assertEqual(linearExp.getExpType(), 'LINEAR')
        self.assertEqual(linearExp.getCoefficient(), '')
        self.assertEqual(linearExp.getOffset(), '')
        self.assertEqual(linearExp.getFrom(), '')
        self.assertEqual(linearExp.getTo(), '')
        self.assertEqual(linearExp.getIterator(), '')
        term1 = linearExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls[0].getUiID()},
                                             {'Value': 'value', 'ClassID': cls[1].getUiID()}], 'VariableID': variable.getUiID()})
        self.assertEqual(linearExp.getTerm2(), {})
        self.assertEqual(linearExp.getChilds(), [])

    # LINEAR EXPRESSION coefficient INT
    def test_LinearExp_coefficient_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable = circuit.Variable('Variable', cls:=circuit.Class('Class', 1))

        linearExp = circuit.LinearExp((variable, 1), coefficient=2)
        
        self.assertIsInstance(linearExp, circuit.LinearExp)
        self.assertEqual(linearExp.getExpType(), 'LINEAR')
        self.assertEqual(linearExp.getCoefficient(), '2')
        self.assertEqual(linearExp.getOffset(), '')
        self.assertEqual(linearExp.getFrom(), '')
        self.assertEqual(linearExp.getTo(), '')
        self.assertEqual(linearExp.getIterator(), '')
        term1 = linearExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()})
        self.assertEqual(linearExp.getTerm2(), {})
        self.assertEqual(linearExp.getChilds(), [])

    # LINEAR EXPRESSION coefficient STRING
    def test_LinearExp_coefficient_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable = circuit.Variable('Variable', cls:=circuit.Class('Class', 1))

        linearExp = circuit.LinearExp((variable, 1), coefficient='coefficient')
        
        self.assertIsInstance(linearExp, circuit.LinearExp)
        self.assertEqual(linearExp.getExpType(), 'LINEAR')
        self.assertEqual(linearExp.getCoefficient(), 'coefficient')
        self.assertEqual(linearExp.getOffset(), '')
        self.assertEqual(linearExp.getFrom(), '')
        self.assertEqual(linearExp.getTo(), '')
        self.assertEqual(linearExp.getIterator(), '')
        term1 = linearExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()})
        self.assertEqual(linearExp.getTerm2(), {})
        self.assertEqual(linearExp.getChilds(), [])

    # BAD ARGUMENT variable
    def test_LinearExp_badArgument_variable(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.LinearExp(())
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT variable[1] LIST
    def test_LinearExp_badArgument_variable1_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable = circuit.Variable('Variable', circuit.Class('Class', 1))

        try:
            circuit.LinearExp((variable, []))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE variable
    def test_LinearExp_badArgumentType_variable(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.LinearExp('variable')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable[0]
    def test_LinearExp_badArgumentType_variable0(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.LinearExp(('variable', 1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable[1] BOOL
    def test_LinearExp_badArgumentType_variable1_bool(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable = circuit.Variable('Variable', circuit.Class('Class', 1))

        try:
            circuit.LinearExp((variable, True))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable[1] LIST
    def test_LinearExp_badArgumentType_variable1_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable = circuit.Variable('Variable', circuit.Class('Class', 1))

        try:
            circuit.LinearExp((variable, [1, True]))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE coefficient
    def test_LinearExp_badArgumentType_coefficient(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable = circuit.Variable('Variable', circuit.Class('Class', 1))

        try:
            circuit.LinearExp((variable, 1), coefficient=True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____QUADRATICEXP_____##################
class Test_QuadraticExp(unittest.TestCase):

    # QUADRATIC EXPRESSION variable1[1] INT
    def test_QuadraticExp_variable11_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', cls1:=circuit.Class('Class1', 1))
        variable2 = circuit.Variable('Variable2', cls2:=circuit.Class('Class2', 1))

        quadraticExp = circuit.QuadraticExp((variable1, 1), (variable2, 2))
        
        self.assertIsInstance(quadraticExp, circuit.QuadraticExp)
        self.assertEqual(quadraticExp.getExpType(), 'QUADRATIC')
        self.assertEqual(quadraticExp.getCoefficient(), '')
        self.assertEqual(quadraticExp.getOffset(), '')
        self.assertEqual(quadraticExp.getFrom(), '')
        self.assertEqual(quadraticExp.getTo(), '')
        self.assertEqual(quadraticExp.getIterator(), '')
        term1 = quadraticExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls1.getUiID()}], 'VariableID': variable1.getUiID()})
        term2 = quadraticExp.getTerm2()
        removeUiID(term2) # remove random uiID to validate behaviour
        self.assertEqual(term2, {'Indexes': [{'Value': '2', 'ClassID': cls2.getUiID()}], 'VariableID': variable2.getUiID()})
        self.assertEqual(quadraticExp.getChilds(), [])

    # QUADRATIC EXPRESSION variable1[1] STRING
    def test_QuadraticExp_variable11_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', cls1:=circuit.Class('Class1', 1))
        variable2 = circuit.Variable('Variable2', cls2:=circuit.Class('Class2', 1))

        quadraticExp = circuit.QuadraticExp((variable1, 'value'), (variable2, 2))
        
        self.assertIsInstance(quadraticExp, circuit.QuadraticExp)
        self.assertEqual(quadraticExp.getExpType(), 'QUADRATIC')
        self.assertEqual(quadraticExp.getCoefficient(), '')
        self.assertEqual(quadraticExp.getOffset(), '')
        self.assertEqual(quadraticExp.getFrom(), '')
        self.assertEqual(quadraticExp.getTo(), '')
        self.assertEqual(quadraticExp.getIterator(), '')
        term1 = quadraticExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': 'value', 'ClassID': cls1.getUiID()}], 'VariableID': variable1.getUiID()})
        term2 = quadraticExp.getTerm2()
        removeUiID(term2) # remove random uiID to validate behaviour
        self.assertEqual(term2, {'Indexes': [{'Value': '2', 'ClassID': cls2.getUiID()}], 'VariableID': variable2.getUiID()})
        self.assertEqual(quadraticExp.getChilds(), [])

    # QUADRATIC EXPRESSION variable1[1] LIST INT, STRING
    def test_QuadraticExp_variable11_list_int_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', cls1:=[circuit.Class('Class1', 1), circuit.Class('Class2', 1)])
        variable2 = circuit.Variable('Variable2', cls2:=circuit.Class('Class3', 1))

        quadraticExp = circuit.QuadraticExp((variable1, [1, 'value']), (variable2, 2))
        
        self.assertIsInstance(quadraticExp, circuit.QuadraticExp)
        self.assertEqual(quadraticExp.getExpType(), 'QUADRATIC')
        self.assertEqual(quadraticExp.getCoefficient(), '')
        self.assertEqual(quadraticExp.getOffset(), '')
        self.assertEqual(quadraticExp.getFrom(), '')
        self.assertEqual(quadraticExp.getTo(), '')
        self.assertEqual(quadraticExp.getIterator(), '')
        term1 = quadraticExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls1[0].getUiID()},
                                             {'Value': 'value', 'ClassID': cls1[1].getUiID()}], 'VariableID': variable1.getUiID()})
        term2 = quadraticExp.getTerm2()
        removeUiID(term2) # remove random uiID to validate behaviour
        self.assertEqual(term2, {'Indexes': [{'Value': '2', 'ClassID': cls2.getUiID()}], 'VariableID': variable2.getUiID()})
        self.assertEqual(quadraticExp.getChilds(), [])

    # QUADRATIC EXPRESSION variable2[1] INT
    def test_QuadraticExp_variable21_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', cls1:=circuit.Class('Class1', 1))
        variable2 = circuit.Variable('Variable2', cls2:=circuit.Class('Class2', 1))

        quadraticExp = circuit.QuadraticExp((variable1, 1), (variable2, 2))
        
        self.assertIsInstance(quadraticExp, circuit.QuadraticExp)
        self.assertEqual(quadraticExp.getExpType(), 'QUADRATIC')
        self.assertEqual(quadraticExp.getCoefficient(), '')
        self.assertEqual(quadraticExp.getOffset(), '')
        self.assertEqual(quadraticExp.getFrom(), '')
        self.assertEqual(quadraticExp.getTo(), '')
        self.assertEqual(quadraticExp.getIterator(), '')
        term1 = quadraticExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls1.getUiID()}], 'VariableID': variable1.getUiID()})
        term2 = quadraticExp.getTerm2()
        removeUiID(term2) # remove random uiID to validate behaviour
        self.assertEqual(term2, {'Indexes': [{'Value': '2', 'ClassID': cls2.getUiID()}], 'VariableID': variable2.getUiID()})
        self.assertEqual(quadraticExp.getChilds(), [])

    # QUADRATIC EXPRESSION variable2[1] STRING
    def test_QuadraticExp_variable21_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', cls1:=circuit.Class('Class1', 1))
        variable2 = circuit.Variable('Variable2', cls2:=circuit.Class('Class2', 1))

        quadraticExp = circuit.QuadraticExp((variable1, 1), (variable2, 'value'))
        
        self.assertIsInstance(quadraticExp, circuit.QuadraticExp)
        self.assertEqual(quadraticExp.getExpType(), 'QUADRATIC')
        self.assertEqual(quadraticExp.getCoefficient(), '')
        self.assertEqual(quadraticExp.getOffset(), '')
        self.assertEqual(quadraticExp.getFrom(), '')
        self.assertEqual(quadraticExp.getTo(), '')
        self.assertEqual(quadraticExp.getIterator(), '')
        term1 = quadraticExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls1.getUiID()}], 'VariableID': variable1.getUiID()})
        term2 = quadraticExp.getTerm2()
        removeUiID(term2) # remove random uiID to validate behaviour
        self.assertEqual(term2, {'Indexes': [{'Value': 'value', 'ClassID': cls2.getUiID()}], 'VariableID': variable2.getUiID()})
        self.assertEqual(quadraticExp.getChilds(), [])

    # QUADRATIC EXPRESSION variable2[1] LIST INT, STRING
    def test_QuadraticExp_variable21_list_int_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', cls1:=circuit.Class('Class1', 1))
        variable2 = circuit.Variable('Variable2', cls2:=[circuit.Class('Class2', 1), circuit.Class('Class3', 1)])

        quadraticExp = circuit.QuadraticExp((variable1, 1), (variable2, [1, 'value']))
        
        self.assertIsInstance(quadraticExp, circuit.QuadraticExp)
        self.assertEqual(quadraticExp.getExpType(), 'QUADRATIC')
        self.assertEqual(quadraticExp.getCoefficient(), '')
        self.assertEqual(quadraticExp.getOffset(), '')
        self.assertEqual(quadraticExp.getFrom(), '')
        self.assertEqual(quadraticExp.getTo(), '')
        self.assertEqual(quadraticExp.getIterator(), '')
        term1 = quadraticExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls1.getUiID()}], 'VariableID': variable1.getUiID()})
        term2 = quadraticExp.getTerm2()
        removeUiID(term2) # remove random uiID to validate behaviour
        self.assertEqual(term2, {'Indexes': [{'Value': '1', 'ClassID': cls2[0].getUiID()},
                                             {'Value': 'value', 'ClassID': cls2[1].getUiID()}], 'VariableID': variable2.getUiID()})
        self.assertEqual(quadraticExp.getChilds(), [])

    # QUADRATIC EXPRESSION coefficient INT
    def test_QuadraticExp_coefficient_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', cls1:=circuit.Class('Class1', 1))
        variable2 = circuit.Variable('Variable2', cls2:=circuit.Class('Class2', 1))

        quadraticExp = circuit.QuadraticExp((variable1, 1), (variable2, 2), coefficient=1)
        
        self.assertIsInstance(quadraticExp, circuit.QuadraticExp)
        self.assertEqual(quadraticExp.getExpType(), 'QUADRATIC')
        self.assertEqual(quadraticExp.getCoefficient(), '1')
        self.assertEqual(quadraticExp.getOffset(), '')
        self.assertEqual(quadraticExp.getFrom(), '')
        self.assertEqual(quadraticExp.getTo(), '')
        self.assertEqual(quadraticExp.getIterator(), '')
        term1 = quadraticExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls1.getUiID()}], 'VariableID': variable1.getUiID()})
        term2 = quadraticExp.getTerm2()
        removeUiID(term2) # remove random uiID to validate behaviour
        self.assertEqual(term2, {'Indexes': [{'Value': '2', 'ClassID': cls2.getUiID()}], 'VariableID': variable2.getUiID()})
        self.assertEqual(quadraticExp.getChilds(), [])

    # QUADRATIC EXPRESSION coefficient STRING
    def test_QuadraticExp_coefficient_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', cls1:=circuit.Class('Class1', 1))
        variable2 = circuit.Variable('Variable2', cls2:=circuit.Class('Class2', 1))

        quadraticExp = circuit.QuadraticExp((variable1, 1), (variable2, 2), coefficient='coefficient')
        
        self.assertIsInstance(quadraticExp, circuit.QuadraticExp)
        self.assertEqual(quadraticExp.getExpType(), 'QUADRATIC')
        self.assertEqual(quadraticExp.getCoefficient(), 'coefficient')
        self.assertEqual(quadraticExp.getOffset(), '')
        self.assertEqual(quadraticExp.getFrom(), '')
        self.assertEqual(quadraticExp.getTo(), '')
        self.assertEqual(quadraticExp.getIterator(), '')
        term1 = quadraticExp.getTerm1()
        removeUiID(term1) # remove random uiID to validate behaviour
        self.assertEqual(term1, {'Indexes': [{'Value': '1', 'ClassID': cls1.getUiID()}], 'VariableID': variable1.getUiID()})
        term2 = quadraticExp.getTerm2()
        removeUiID(term2) # remove random uiID to validate behaviour
        self.assertEqual(term2, {'Indexes': [{'Value': '2', 'ClassID': cls2.getUiID()}], 'VariableID': variable2.getUiID()})
        self.assertEqual(quadraticExp.getChilds(), [])

    # BAD ARGUMENT variable1
    def test_QuadraticExp_badArgument_variable1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((), (variable2, 2))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT variable1[1] LIST
    def test_QuadraticExp_badArgument_variable11_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', circuit.Class('Class', 1))
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, []), (variable2, 1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT variable2
    def test_QuadraticExp_badArgument_variable2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, 1), ())
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT variable2[1] LIST
    def test_QuadraticExp_badArgument_variable21_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', circuit.Class('Class', 1))
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, 1), (variable2, []))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE variable1
    def test_QuadraticExp_badArgumentType_variable1(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp('variable1', (variable2, 1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable1[0]
    def test_QuadraticExp_badArgumentType_variable10(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp(('variable1', 1), (variable2, 1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable1[1] BOOL
    def test_QuadraticExp_badArgumentType_variable11_bool(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable', circuit.Class('Class', 1))
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, True), (variable2, 1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
    # BAD ARGUMENT TYPE variable1[1] LIST
    def test_QuadraticExp_badArgumentType_variable11_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable', circuit.Class('Class', 1))
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, [1, True]), (variable2, 1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable2
    def test_QuadraticExp_badArgumentType_variable2(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, 1), 'variable2')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable2[0]
    def test_QuadraticExp_badArgumentType_variable20(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, 1), ('variable2', 1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable2[1] BOOL
    def test_QuadraticExp_badArgumentType_variable21_bool(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', circuit.Class('Class', 1))
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, 1), (variable2, True))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable2[1] LIST
    def test_QuadraticExp_badArgumentType_variable21_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', circuit.Class('Class', 1))
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, 1), (variable2, [1, True]))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE coefficient
    def test_QuadraticExp_badArgumentType_coefficient(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        variable1 = circuit.Variable('Variable1', circuit.Class('Class', 1))
        variable2 = circuit.Variable('Variable2', circuit.Class('Class', 1))

        try:
            circuit.QuadraticExp((variable1, 1), (variable2, 1), coefficient=True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____SQUAREDEXP_____##################
class Test_SquaredExp(unittest.TestCase):

    # SQUARED EXPRESSION expression OFFSETEXP
    def test_SquaredExp_expression_OffsetExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        squaredExp = circuit.SquaredExp(offsetExp)
        
        self.assertIsInstance(squaredExp, circuit.SquaredExp)
        self.assertEqual(squaredExp.getExpType(), 'SQUARED')
        self.assertEqual(squaredExp.getCoefficient(), '')
        self.assertEqual(squaredExp.getOffset(), '')
        self.assertEqual(squaredExp.getFrom(), '')
        self.assertEqual(squaredExp.getTo(), '')
        self.assertEqual(squaredExp.getIterator(), '')
        self.assertEqual(squaredExp.getTerm1(), {})
        self.assertEqual(squaredExp.getTerm2(), {})
        self.assertEqual(squaredExp.getChilds(), [{
            'uiID': offsetExp.getUiID(),
            'Type': offsetExp.getExpType(),
            'Coefficient': offsetExp.getCoefficient(),
            'Offset': offsetExp.getOffset(),
            'From': offsetExp.getFrom(),
            'To': offsetExp.getTo(),
            'Iterator': offsetExp.getIterator(),
            'Term1': offsetExp.getTerm1(),
            'Term2': offsetExp.getTerm2(),
            'Childs': offsetExp.getChilds()
        }])

    # SQUARED EXPRESSION expression LINEAREXP
    def test_SquaredExp_expression_LinearExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        linearExp = circuit.LinearExp((circuit.Variable('Variable', circuit.Class('Class', 1)), 1))

        squaredExp = circuit.SquaredExp(linearExp)
        
        self.assertIsInstance(squaredExp, circuit.SquaredExp)
        self.assertEqual(squaredExp.getExpType(), 'SQUARED')
        self.assertEqual(squaredExp.getCoefficient(), '')
        self.assertEqual(squaredExp.getOffset(), '')
        self.assertEqual(squaredExp.getFrom(), '')
        self.assertEqual(squaredExp.getTo(), '')
        self.assertEqual(squaredExp.getIterator(), '')
        self.assertEqual(squaredExp.getTerm1(), {})
        self.assertEqual(squaredExp.getTerm2(), {})
        self.assertEqual(squaredExp.getChilds(), [{
            'uiID': linearExp.getUiID(),
            'Type': linearExp.getExpType(),
            'Coefficient': linearExp.getCoefficient(),
            'Offset': linearExp.getOffset(),
            'From': linearExp.getFrom(),
            'To': linearExp.getTo(),
            'Iterator': linearExp.getIterator(),
            'Term1': linearExp.getTerm1(),
            'Term2': linearExp.getTerm2(),
            'Childs': linearExp.getChilds()
        }])

    # SQUARED EXPRESSION expression SUMMATORYEXP
    def test_SquaredExp_expression_SummatoryExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        summatory = circuit.SummatoryExp(1, 2, circuit.OffsetExp(1))

        squaredExp = circuit.SquaredExp(summatory)
        
        self.assertIsInstance(squaredExp, circuit.SquaredExp)
        self.assertEqual(squaredExp.getExpType(), 'SQUARED')
        self.assertEqual(squaredExp.getCoefficient(), '')
        self.assertEqual(squaredExp.getOffset(), '')
        self.assertEqual(squaredExp.getFrom(), '')
        self.assertEqual(squaredExp.getTo(), '')
        self.assertEqual(squaredExp.getIterator(), '')
        self.assertEqual(squaredExp.getTerm1(), {})
        self.assertEqual(squaredExp.getTerm2(), {})
        self.assertEqual(squaredExp.getChilds(), [{
            'uiID': summatory.getUiID(),
            'Type': summatory.getExpType(),
            'Coefficient': summatory.getCoefficient(),
            'Offset': summatory.getOffset(),
            'From': summatory.getFrom(),
            'To': summatory.getTo(),
            'Iterator': summatory.getIterator(),
            'Term1': summatory.getTerm1(),
            'Term2': summatory.getTerm2(),
            'Childs': summatory.getChilds()
        }])

    # SQUARED EXPRESSION expression LIST OFFSETEXP, LINEAREXP, SUMMATORYEXP
    def test_SquaredExp_expression_list_OffsetExp_LinearExp_SummatoryExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)
        linearExp = circuit.LinearExp((circuit.Variable('Variable', circuit.Class('Class', 1)), 1))
        summatory = circuit.SummatoryExp(1, 2, offsetExp)

        squaredExp = circuit.SquaredExp([offsetExp, linearExp, summatory])
        
        self.assertIsInstance(squaredExp, circuit.SquaredExp)
        self.assertEqual(squaredExp.getExpType(), 'SQUARED')
        self.assertEqual(squaredExp.getCoefficient(), '')
        self.assertEqual(squaredExp.getOffset(), '')
        self.assertEqual(squaredExp.getFrom(), '')
        self.assertEqual(squaredExp.getTo(), '')
        self.assertEqual(squaredExp.getIterator(), '')
        self.assertEqual(squaredExp.getTerm1(), {})
        self.assertEqual(squaredExp.getTerm2(), {})
        self.assertEqual(squaredExp.getChilds(), [{
            'uiID': offsetExp.getUiID(),
            'Type': offsetExp.getExpType(),
            'Coefficient': offsetExp.getCoefficient(),
            'Offset': offsetExp.getOffset(),
            'From': offsetExp.getFrom(),
            'To': offsetExp.getTo(),
            'Iterator': offsetExp.getIterator(),
            'Term1': offsetExp.getTerm1(),
            'Term2': offsetExp.getTerm2(),
            'Childs': offsetExp.getChilds()
        },
        {
            'uiID': linearExp.getUiID(),
            'Type': linearExp.getExpType(),
            'Coefficient': linearExp.getCoefficient(),
            'Offset': linearExp.getOffset(),
            'From': linearExp.getFrom(),
            'To': linearExp.getTo(),
            'Iterator': linearExp.getIterator(),
            'Term1': linearExp.getTerm1(),
            'Term2': linearExp.getTerm2(),
            'Childs': linearExp.getChilds()
        },
        {
            'uiID': summatory.getUiID(),
            'Type': summatory.getExpType(),
            'Coefficient': summatory.getCoefficient(),
            'Offset': summatory.getOffset(),
            'From': summatory.getFrom(),
            'To': summatory.getTo(),
            'Iterator': summatory.getIterator(),
            'Term1': summatory.getTerm1(),
            'Term2': summatory.getTerm2(),
            'Childs': summatory.getChilds()
        }])

    # BAD ARGUMENT expression LIST
    def test_SquaredExp_badArgument_expression_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.SquaredExp([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE expression STRING
    def test_SquaredExp_badArgumentType_expression_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.SquaredExp('expression')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE expression LIST
    def test_SquaredExp_badArgumentType_expression_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        try:
            circuit.SquaredExp([offsetExp, 'expression'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____SUMMATORYEXP_____##################
class Test_SummatoryExp(unittest.TestCase):

    # SUMMATORY EXPRESSION fromValue INT
    def test_SummatoryExp_fromValue_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        summatory = circuit.SummatoryExp(1, 2, offsetExp)
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': offsetExp.getUiID(),
            'Type': offsetExp.getExpType(),
            'Coefficient': offsetExp.getCoefficient(),
            'Offset': offsetExp.getOffset(),
            'From': offsetExp.getFrom(),
            'To': offsetExp.getTo(),
            'Iterator': offsetExp.getIterator(),
            'Term1': offsetExp.getTerm1(),
            'Term2': offsetExp.getTerm2(),
            'Childs': offsetExp.getChilds()
        }])

    # SUMMATORY EXPRESSION fromValue STRING
    def test_SummatoryExp_fromValue_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        summatory = circuit.SummatoryExp('fromValue', 2, offsetExp)
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), 'fromValue')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': offsetExp.getUiID(),
            'Type': offsetExp.getExpType(),
            'Coefficient': offsetExp.getCoefficient(),
            'Offset': offsetExp.getOffset(),
            'From': offsetExp.getFrom(),
            'To': offsetExp.getTo(),
            'Iterator': offsetExp.getIterator(),
            'Term1': offsetExp.getTerm1(),
            'Term2': offsetExp.getTerm2(),
            'Childs': offsetExp.getChilds()
        }])

    # SUMMATORY EXPRESSION toValue INT
    def test_SummatoryExp_toValue_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        summatory = circuit.SummatoryExp(1, 2, offsetExp)
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': offsetExp.getUiID(),
            'Type': offsetExp.getExpType(),
            'Coefficient': offsetExp.getCoefficient(),
            'Offset': offsetExp.getOffset(),
            'From': offsetExp.getFrom(),
            'To': offsetExp.getTo(),
            'Iterator': offsetExp.getIterator(),
            'Term1': offsetExp.getTerm1(),
            'Term2': offsetExp.getTerm2(),
            'Childs': offsetExp.getChilds()
        }])

    # SUMMATORY EXPRESSION toValue STRING
    def test_SummatoryExp_toValue_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        summatory = circuit.SummatoryExp(1, 'toValue', offsetExp)
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), 'toValue')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': offsetExp.getUiID(),
            'Type': offsetExp.getExpType(),
            'Coefficient': offsetExp.getCoefficient(),
            'Offset': offsetExp.getOffset(),
            'From': offsetExp.getFrom(),
            'To': offsetExp.getTo(),
            'Iterator': offsetExp.getIterator(),
            'Term1': offsetExp.getTerm1(),
            'Term2': offsetExp.getTerm2(),
            'Childs': offsetExp.getChilds()
        }])

    # SUMMATORY EXPRESSION expression OFFSETEXP
    def test_SummatoryExp_expression_OffsetExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        summatory = circuit.SummatoryExp(1, 2, offsetExp)
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': offsetExp.getUiID(),
            'Type': offsetExp.getExpType(),
            'Coefficient': offsetExp.getCoefficient(),
            'Offset': offsetExp.getOffset(),
            'From': offsetExp.getFrom(),
            'To': offsetExp.getTo(),
            'Iterator': offsetExp.getIterator(),
            'Term1': offsetExp.getTerm1(),
            'Term2': offsetExp.getTerm2(),
            'Childs': offsetExp.getChilds()
        }])

    # SUMMATORY EXPRESSION expression LINEAREXP
    def test_SummatoryExp_expression_LinearExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        linearExp = circuit.LinearExp((circuit.Variable('Variable', circuit.Class('Class', 1)), 1))

        summatory = circuit.SummatoryExp(1, 2, linearExp)
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': linearExp.getUiID(),
            'Type': linearExp.getExpType(),
            'Coefficient': linearExp.getCoefficient(),
            'Offset': linearExp.getOffset(),
            'From': linearExp.getFrom(),
            'To': linearExp.getTo(),
            'Iterator': linearExp.getIterator(),
            'Term1': linearExp.getTerm1(),
            'Term2': linearExp.getTerm2(),
            'Childs': linearExp.getChilds()
        }])

    # SUMMATORY EXPRESSION expression QUADRATICEXP
    def test_SummatoryExp_expression_QuadraticExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        quadraticExp = circuit.QuadraticExp((variable:=circuit.Variable('Variable', circuit.Class('Class', 1)), 1), (variable, 2))

        summatory = circuit.SummatoryExp(1, 2, quadraticExp)
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': quadraticExp.getUiID(),
            'Type': quadraticExp.getExpType(),
            'Coefficient': quadraticExp.getCoefficient(),
            'Offset': quadraticExp.getOffset(),
            'From': quadraticExp.getFrom(),
            'To': quadraticExp.getTo(),
            'Iterator': quadraticExp.getIterator(),
            'Term1': quadraticExp.getTerm1(),
            'Term2': quadraticExp.getTerm2(),
            'Childs': quadraticExp.getChilds()
        }])

    # SUMMATORY EXPRESSION expression SQUAREDEXP
    def test_SummatoryExp_expression_SquaredExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        squaredExp = circuit.SquaredExp(circuit.OffsetExp(1))

        summatory = circuit.SummatoryExp(1, 2, squaredExp)
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': squaredExp.getUiID(),
            'Type': squaredExp.getExpType(),
            'Coefficient': squaredExp.getCoefficient(),
            'Offset': squaredExp.getOffset(),
            'From': squaredExp.getFrom(),
            'To': squaredExp.getTo(),
            'Iterator': squaredExp.getIterator(),
            'Term1': squaredExp.getTerm1(),
            'Term2': squaredExp.getTerm2(),
            'Childs': squaredExp.getChilds()
        }])

    # SUMMATORY EXPRESSION expression SUMMATORYEXP
    def test_SummatoryExp_expression_SummatoryExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        summatory1 = circuit.SummatoryExp(1, 2, circuit.OffsetExp(1))

        summatory = circuit.SummatoryExp(1, 2, summatory1)
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': summatory1.getUiID(),
            'Type': summatory1.getExpType(),
            'Coefficient': summatory1.getCoefficient(),
            'Offset': summatory1.getOffset(),
            'From': summatory1.getFrom(),
            'To': summatory1.getTo(),
            'Iterator': summatory1.getIterator(),
            'Term1': summatory1.getTerm1(),
            'Term2': summatory1.getTerm2(),
            'Childs': summatory1.getChilds()
        }])

    # SUMMATORY EXPRESSION expression LIST OFFSETEXP, LINEAREXP, QUADRATICEXP, SQUAREDEXP, SUMMATORYEXP
    def test_SummatoryExp_expression_list_OffsetExp_LinearExp_QuadraticExp_SquaredExp_SummatoryExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)
        linearExp = circuit.LinearExp((variable:=circuit.Variable('Variable', circuit.Class('Class', 1)), 1))
        quadraticExp = circuit.QuadraticExp((variable, 1), (variable, 2))
        squaredExp = circuit.SquaredExp(offsetExp)
        summatory1 = circuit.SummatoryExp(1, 2, offsetExp)

        summatory = circuit.SummatoryExp(1, 2, [offsetExp, linearExp, quadraticExp, squaredExp, summatory1])
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'i')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': offsetExp.getUiID(),
            'Type': offsetExp.getExpType(),
            'Coefficient': offsetExp.getCoefficient(),
            'Offset': offsetExp.getOffset(),
            'From': offsetExp.getFrom(),
            'To': offsetExp.getTo(),
            'Iterator': offsetExp.getIterator(),
            'Term1': offsetExp.getTerm1(),
            'Term2': offsetExp.getTerm2(),
            'Childs': offsetExp.getChilds()
        },
        {
            'uiID': linearExp.getUiID(),
            'Type': linearExp.getExpType(),
            'Coefficient': linearExp.getCoefficient(),
            'Offset': linearExp.getOffset(),
            'From': linearExp.getFrom(),
            'To': linearExp.getTo(),
            'Iterator': linearExp.getIterator(),
            'Term1': linearExp.getTerm1(),
            'Term2': linearExp.getTerm2(),
            'Childs': linearExp.getChilds()
        },
        {
            'uiID': quadraticExp.getUiID(),
            'Type': quadraticExp.getExpType(),
            'Coefficient': quadraticExp.getCoefficient(),
            'Offset': quadraticExp.getOffset(),
            'From': quadraticExp.getFrom(),
            'To': quadraticExp.getTo(),
            'Iterator': quadraticExp.getIterator(),
            'Term1': quadraticExp.getTerm1(),
            'Term2': quadraticExp.getTerm2(),
            'Childs': quadraticExp.getChilds()
        },
        {
            'uiID': squaredExp.getUiID(),
            'Type': squaredExp.getExpType(),
            'Coefficient': squaredExp.getCoefficient(),
            'Offset': squaredExp.getOffset(),
            'From': squaredExp.getFrom(),
            'To': squaredExp.getTo(),
            'Iterator': squaredExp.getIterator(),
            'Term1': squaredExp.getTerm1(),
            'Term2': squaredExp.getTerm2(),
            'Childs': squaredExp.getChilds()
        },
        {
            'uiID': summatory1.getUiID(),
            'Type': summatory1.getExpType(),
            'Coefficient': summatory1.getCoefficient(),
            'Offset': summatory1.getOffset(),
            'From': summatory1.getFrom(),
            'To': summatory1.getTo(),
            'Iterator': summatory1.getIterator(),
            'Term1': summatory1.getTerm1(),
            'Term2': summatory1.getTerm2(),
            'Childs': summatory1.getChilds()
        }])

    # SUMMATORY EXPRESSION iterator
    def test_SummatoryExp_iterator(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        summatory = circuit.SummatoryExp(1, 2, offsetExp, iterator='x')
        
        self.assertIsInstance(summatory, circuit.SummatoryExp)
        self.assertEqual(summatory.getExpType(), 'SUMMATORY')
        self.assertEqual(summatory.getCoefficient(), '')
        self.assertEqual(summatory.getOffset(), '')
        self.assertEqual(summatory.getFrom(), '1')
        self.assertEqual(summatory.getTo(), '2')
        self.assertEqual(summatory.getIterator(), 'x')
        self.assertEqual(summatory.getTerm1(), {})
        self.assertEqual(summatory.getTerm2(), {})
        self.assertEqual(summatory.getChilds(), [{
            'uiID': offsetExp.getUiID(),
            'Type': offsetExp.getExpType(),
            'Coefficient': offsetExp.getCoefficient(),
            'Offset': offsetExp.getOffset(),
            'From': offsetExp.getFrom(),
            'To': offsetExp.getTo(),
            'Iterator': offsetExp.getIterator(),
            'Term1': offsetExp.getTerm1(),
            'Term2': offsetExp.getTerm2(),
            'Childs': offsetExp.getChilds()
        }])

    # BAD ARGUMENT expression LIST
    def test_SummatoryExp_badArgument_expression_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.SummatoryExp(1, 2, [])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE fromValue
    def test_SummatoryExp_badArgumentType_fromValue(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        try:
            circuit.SummatoryExp(True, 2, offsetExp)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE toValue
    def test_SummatoryExp_badArgumentType_toValue(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        try:
            circuit.SummatoryExp(1, True, offsetExp)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE expression STRING
    def test_SummatoryExp_badArgumentType_expression_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.SummatoryExp(1, 2, 'expression')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE expression LIST
    def test_SummatoryExp_badArgumentType_expression_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        try:
            circuit.SummatoryExp(1, 2, [offsetExp, 1])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE iterator
    def test_SummatoryExp_badArgumentType_iterator(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        offsetExp = circuit.OffsetExp(1)

        try:
            circuit.SummatoryExp(1, 2, offsetExp, iterator=99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ADD PARAMETER_____##################
class Test_AddParameter(unittest.TestCase):

    # ADD PARAMETER parameter PARAMETER
    def test_addParameter_parameter_Parameter(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        parameter = circuit.Parameter('Parameter', 1)

        parameterAdded = circuit.addParameter(parameter)

        circuitParameters = circuit.getParameters()
        removeUiID(circuitParameters) # remove random uiID to validate behaviour

        self.assertIsInstance(parameterAdded, qsoa.CircuitAnnealing.Parameter)
        self.assertIsInstance(circuitParameters, list)
        self.assertEqual(circuitParameters, [{'Name': 'Parameter', 'Value': '1'}])

    # ADD PARAMETER parameter LIST
    def test_addParameter_parameter_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        parameter1 = circuit.Parameter('Parameter1', 1)
        parameter2 = circuit.Parameter('Parameter2', 2)

        circuit = qsoa.CircuitAnnealing()

        parameterAdded = circuit.addParameter([parameter1, parameter2])

        circuitParameters = circuit.getParameters()
        removeUiID(circuitParameters) # remove random uiID to validate behaviour

        self.assertIsInstance(parameterAdded, list)
        for p in parameterAdded: self.assertIsInstance(p, qsoa.CircuitAnnealing.Parameter)
        self.assertIsInstance(circuitParameters, list)
        self.assertEqual(circuitParameters, [{'Name': 'Parameter1', 'Value': '1'}, {'Name': 'Parameter2', 'Value': '2'}])

    # BAD ARGUMENT parameter LIST
    def test_addParameter_badArgument_parameter_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addParameter([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE parameter STRING
    def test_addParameter_badArgumentType_parameter_string(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addParameter('parameter')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
        
    # BAD ARGUMENT TYPE parameter LIST
    def test_addParameter_badArgumentType_parameter_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        parameter = circuit.Parameter('Parameter', 1)

        try:
            circuit.addParameter([parameter, 'parameter'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

##################_____ADD AUXILIARY DATA_____##################
class Test_AddAuxData(unittest.TestCase):

    # ADD AUXDATA
    def test_addAuxData(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        auxData = circuit.AuxData('AuxData', 1)

        auxDataAdded = circuit.addAuxData(auxData)

        circuitAuxData = circuit.getAuxData()
        removeUiID(circuitAuxData) # remove random uiID to validate behaviour

        self.assertIsInstance(auxDataAdded, qsoa.CircuitAnnealing.AuxData)
        self.assertIsInstance(circuitAuxData, list)
        self.assertEqual(circuitAuxData, [{'Name': 'AuxData', 'Value': '1'}])

    # ADD AUXDATA LIST
    def test_addAuxData_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        auxData1 = circuit.AuxData('AuxData1', 1)
        auxData2 = circuit.AuxData('AuxData2', 2)

        auxDataAdded = circuit.addAuxData([auxData1, auxData2])

        circuitAuxData = circuit.getAuxData()
        removeUiID(circuitAuxData) # remove random uiID to validate behaviour

        self.assertIsInstance(auxDataAdded, list)
        for a in auxDataAdded: self.assertIsInstance(a, qsoa.CircuitAnnealing.AuxData)
        self.assertIsInstance(circuitAuxData, list)
        self.assertEqual(circuitAuxData, [{'Name': 'AuxData1', 'Value': '1'}, {'Name': 'AuxData2', 'Value': '2'}])

    # BAD ARGUMENT auxData LIST
    def test_addAuxData_badArgument_auxData_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addAuxData([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE auxData
    def test_addAuxData_badArgumentType_auxData(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addAuxData('auxData')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE parameter LIST
    def test_addAuxData_badArgumentType_parameter_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        auxData = circuit.AuxData('AuxData', 1)

        try:
            circuit.addAuxData([auxData, 'auxData'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ADD CLASS_____##################
class Test_AddClass(unittest.TestCase):

    # ADD CLASS
    def test_addClass(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 2)

        clsAdded = circuit.addClass(cls)

        circuitClasses = circuit.getClasses()
        removeUiID(circuitClasses) # remove random uiID to validate behaviour

        self.assertIsInstance(clsAdded, qsoa.CircuitAnnealing.Class)
        self.assertIsInstance(circuitClasses, list)
        self.assertEqual(circuitClasses, [{'Description': '', 'Name': 'Class', 'NumberOfVars': '2', 'Properties': []}])

    # ADD CLASS LIST
    def test_addClass_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls1 = circuit.Class('Class1', 1)
        cls2 = circuit.Class('Class2', 2)

        clsAdded = circuit.addClass([cls1, cls2])

        circuitClasses = circuit.getClasses()
        removeUiID(circuitClasses) # remove random uiID to validate behaviour

        self.assertIsInstance(clsAdded, list)
        for c in clsAdded: self.assertIsInstance(c, qsoa.CircuitAnnealing.Class)
        self.assertIsInstance(circuitClasses, list)
        self.assertEqual(circuitClasses, [{'Description': '', 'Name': 'Class1', 'NumberOfVars': '1', 'Properties': []},
                                          {'Description': '', 'Name': 'Class2', 'NumberOfVars': '2', 'Properties': []}])

    # BAD ARGUMENT cls LIST
    def test_addClass_badArgument_cls_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addClass([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE cls
    def test_addClass_badArgumentType_cls(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addClass('cls')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE cls LIST
    def test_addClass_badArgumentType_cls_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 2)

        try:
            circuit.addAuxData([cls, 'cls'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ADD VARIABLE_____##################
class Test_AddVariable(unittest.TestCase):

    # ADD VARIABLE
    def test_addVariable(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 1)
        variable = circuit.Variable('Variable', [cls])

        variableAdded = circuit.addVariable(variable)

        circuitVariables = circuit.getVariables()
        removeUiID(circuitVariables) # remove random uiID to validate behaviour

        self.assertIsInstance(variableAdded, qsoa.CircuitAnnealing.Variable)
        self.assertIsInstance(circuitVariables, list)
        self.assertEqual(circuitVariables, [{'Classes': [cls.getUiID()], 'Description': '', 'Name': 'Variable'}])

    # ADD VARIABLE LIST
    def test_addVariable_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 1)
        variable1 = circuit.Variable('Variable1', cls)
        variable2 = circuit.Variable('Variable2', cls)

        variableAdded = circuit.addVariable([variable1, variable2])

        circuitVariables = circuit.getVariables()
        removeUiID(circuitVariables) # remove random uiID to validate behaviour

        self.assertIsInstance(variableAdded, list)
        for v in variableAdded: self.assertIsInstance(v, qsoa.CircuitAnnealing.Variable)
        self.assertIsInstance(circuitVariables, list)
        self.assertEqual(circuitVariables, [{'Classes': [cls.getUiID()], 'Description': '', 'Name': 'Variable1'},
                                            {'Classes': [cls.getUiID()], 'Description': '', 'Name': 'Variable2'}])

    # BAD ARGUMENT variable LIST
    def test_addVariable_badArgument_variable_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addVariable([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE variable
    def test_addVariable_badArgumentType_variable(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addVariable('variable')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE variable LIST
    def test_addVariable_badArgumentType_variable_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        cls = circuit.Class('Class', 1)
        variable = circuit.Variable('Variable', cls)

        try:
            circuit.addVariable([variable, 'variable'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ADD RULE_____##################
class Test_AddRule(unittest.TestCase):

    # ADD RULE
    def test_addRule(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)

        ruleAdded = circuit.addRule(rule)

        rules = circuit.getRules()
        removeUiID(rules) # remove random uiID to validate behaviour

        self.assertIsInstance(ruleAdded, qsoa.CircuitAnnealing.Rule)
        self.assertIsInstance(rules, list)
        self.assertEqual(rules, [{'Expressions': [], 'Name': 'Rule', 'Lambda': '1', 'Description': '', 'Disabled': 'False'}])

    # ADD RULE LIST
    def test_addRule_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule1 = circuit.Rule('Rule1', 1)
        rule2 = circuit.Rule('Rule2', 2)

        ruleAdded = circuit.addRule([rule1, rule2])

        rules = circuit.getRules()
        removeUiID(rules) # remove random uiID to validate behaviour

        self.assertIsInstance(ruleAdded, list)
        for r in ruleAdded: self.assertIsInstance(r, qsoa.CircuitAnnealing.Rule)
        self.assertIsInstance(rules, list)
        self.assertEqual(rules, [{'Expressions': [], 'Name': 'Rule1', 'Lambda': '1', 'Description': '', 'Disabled': 'False'},
                                 {'Expressions': [], 'Name': 'Rule2', 'Lambda': '2', 'Description': '', 'Disabled': 'False'}])

    # BAD ARGUMENT rule LIST
    def test_addRule_badArgument_rule_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addRule([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE rule
    def test_addRule_badArgumentType_rule(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()

        try:
            circuit.addRule('rule')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE rule LIST
    def test_addVariable_badArgumentType_rule_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)

        try:
            circuit.addVariable([rule, 'rule'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ADD EXPRESSION_____##################
class Test_AddExpression(unittest.TestCase):

    # ADD EXPRESSION expression OFFSETEXP
    def test_addExpression_expression_OffsetExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)
        offsetExp = circuit.OffsetExp(1)

        ruleAdded = rule.addExpression(offsetExp)

        expressions = rule.getExpressions()
        removeUiID(expressions) # remove random uiID to validate behaviour

        self.assertIsInstance(ruleAdded, qsoa.CircuitAnnealing.Rule)
        self.assertIsInstance(expressions, list)
        self.assertEqual(expressions, [{'Type': 'OFFSET', 'Coefficient': '', 'Offset': '1', 'From': '', 'To': '', 'Iterator': '', 'Term1': {}, 'Term2': {}, 'Childs': []}])

    # ADD EXPRESSION expression LINEAREXP
    def test_addExpression_expression_LinearExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)
        linearExp = circuit.LinearExp((variable:=circuit.Variable('Variable', cls:=circuit.Class('Class', 1)), 1))

        ruleAdded = rule.addExpression(linearExp)

        expressions = rule.getExpressions()

        self.assertIsInstance(ruleAdded, qsoa.CircuitAnnealing.Rule)
        self.assertIsInstance(expressions, list)
        removeUiID(expressions) # remove random uiID to validate behaviour
        self.assertEqual(expressions, [{'Type': 'LINEAR', 'Coefficient': '', 'Offset': '', 'From': '', 'To': '', 'Iterator': '',
                                        'Term1': {'Indexes': [{'Value': '1', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()},
                                        'Term2': {}, 'Childs': []}])

    # ADD EXPRESSION expression QUADRATICEXP
    def test_addExpression_expression_QuadraticExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)
        quadraticExp = circuit.QuadraticExp((variable:=circuit.Variable('Variable1', cls:=circuit.Class('Class1', 1)), 1), (variable, 2))

        ruleAdded = rule.addExpression(quadraticExp)

        expressions = rule.getExpressions()

        self.assertIsInstance(ruleAdded, qsoa.CircuitAnnealing.Rule)
        self.assertIsInstance(expressions, list)
        removeUiID(expressions) # remove random uiID to validate behaviour
        self.assertEqual(expressions, [{'Type': 'QUADRATIC', 'Coefficient': '', 'Offset': '', 'From': '', 'To': '', 'Iterator': '',
                                        'Term1': {'Indexes': [{'Value': '1', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()},
                                        'Term2': {'Indexes': [{'Value': '2', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()}, 'Childs': []}])

    # ADD EXPRESSION expression SQUAREDEXP
    def test_addExpression_expression_SquaredExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)
        squaredExp = circuit.SquaredExp(circuit.OffsetExp(1))
        
        ruleAdded = rule.addExpression(squaredExp)

        expressions = rule.getExpressions()

        self.assertIsInstance(ruleAdded, qsoa.CircuitAnnealing.Rule)
        self.assertIsInstance(expressions, list)
        removeUiID(expressions) # remove random uiID to validate behaviour
        self.assertEqual(expressions, [{'Type': 'SQUARED', 'Coefficient': '', 'Offset': '', 'From': '', 'To': '', 'Iterator': '', 'Term1': {}, 'Term2': {},
                                        'Childs': [{'Type': 'OFFSET', 'Coefficient': '', 'Offset': '1', 'From': '', 'To': '', 'Iterator': '', 'Term1': {}, 'Term2': {}, 'Childs': []}]}])

    # ADD EXPRESSION expression SQUAREDEXP
    def test_addExpression_expression_SquaredExp(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)
        summatory = circuit.SummatoryExp(1, 2, circuit.OffsetExp(1))
        
        ruleAdded = rule.addExpression(summatory)

        expressions = rule.getExpressions()

        self.assertIsInstance(ruleAdded, qsoa.CircuitAnnealing.Rule)
        self.assertIsInstance(expressions, list)
        removeUiID(expressions) # remove random uiID to validate behaviour
        self.assertEqual(expressions, [{'Type': 'SUMMATORY', 'Coefficient': '', 'Offset': '', 'From': '1', 'To': '2', 'Iterator': 'i', 'Term1': {}, 'Term2': {},
                                        'Childs': [{'Type': 'OFFSET', 'Coefficient': '', 'Offset': '1', 'From': '', 'To': '', 'Iterator': '', 'Term1': {}, 'Term2': {}, 'Childs': []}]}])

    # ADD EXPRESSION LIST OFFSETEXP, LINEAREXP, QUADRATICEXP, SQUAREDEXP, SUMMATORYEXP
    def test_addExpression_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)
        offsetExp = circuit.OffsetExp(1)
        linearExp = circuit.LinearExp((variable:=circuit.Variable('Variable', cls:=circuit.Class('Class', 1)), 1))
        quadraticExp = circuit.QuadraticExp((variable, 1), (variable, 2))
        squaredExp = circuit.SquaredExp(offsetExp)
        summatory = circuit.SummatoryExp(1, 2, offsetExp)

        ruleAdded = rule.addExpression([offsetExp, linearExp, quadraticExp, squaredExp, summatory])

        expressions = rule.getExpressions()
        self.assertIsInstance(ruleAdded, qsoa.CircuitAnnealing.Rule)
        self.assertIsInstance(expressions, list)
        removeUiID(expressions) # remove random uiID to validate behaviour
        self.assertEqual(expressions, [{'Type': 'OFFSET', 'Coefficient': '', 'Offset': '1', 'From': '', 'To': '', 'Iterator': '', 'Term1': {}, 'Term2': {}, 'Childs': []},
                                       {'Type': 'LINEAR', 'Coefficient': '', 'Offset': '', 'From': '', 'To': '', 'Iterator': '',
                                        'Term1': {'Indexes': [{'Value': '1', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()},
                                        'Term2': {}, 'Childs': []}, 
                                       {'Type': 'QUADRATIC', 'Coefficient': '', 'Offset': '', 'From': '', 'To': '', 'Iterator': '',
                                        'Term1': {'Indexes': [{'Value': '1', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()},
                                        'Term2': {'Indexes': [{'Value': '2', 'ClassID': cls.getUiID()}], 'VariableID': variable.getUiID()}, 'Childs': []},
                                       {'Type': 'SQUARED', 'Coefficient': '', 'Offset': '', 'From': '', 'To': '', 'Iterator': '', 'Term1': {}, 'Term2': {},
                                        'Childs': [{'Type': 'OFFSET', 'Coefficient': '', 'Offset': '1', 'From': '', 'To': '', 'Iterator': '', 'Term1': {}, 'Term2': {}, 'Childs': []}]},
                                       {'Type': 'SUMMATORY', 'Coefficient': '', 'Offset': '', 'From': '1', 'To': '2', 'Iterator': 'i', 'Term1': {}, 'Term2': {},
                                        'Childs': [{'Type': 'OFFSET', 'Coefficient': '', 'Offset': '1', 'From': '', 'To': '', 'Iterator': '', 'Term1': {}, 'Term2': {}, 'Childs': []}]}])

    # BAD ARGUMENT expression LIST
    def test_addExpression_badArgument_expression_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)

        try:
            rule.addExpression([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE expression
    def test_addExpression_badArgumentType_expression(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)

        try:
            rule.addExpression('expression')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE rule LIST
    def test_addVariable_badArgumentType_rule_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitAnnealing()
        rule = circuit.Rule('Rule', 1)
        offsetExp = circuit.OffsetExp(1)

        try:
            rule.addExpression([offsetExp, 'expression'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()