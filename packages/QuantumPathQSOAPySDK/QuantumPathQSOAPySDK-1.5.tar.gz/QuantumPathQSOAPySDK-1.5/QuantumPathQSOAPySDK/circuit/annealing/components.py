from ...utils.checker import (checkInputTypes, checkMathExpression)
import uuid


##################_____PRIVATE CLASSES_____##################

# EXPRESSION
class __Expression():

    # CONSTRUCTOR
    def __init__(self, expType: str, coefficient: str = '', offset: str = '', fromValue: str = '', toValue: str = '',
                    iterator: str = '', term1: dict = {}, term2: dict = {}, childs: list = []):
        self.__uiID = str(uuid.uuid4())
        self.__expType = expType
        self.__coefficient = coefficient
        self.__offset = offset
        self.__from = fromValue
        self.__to = toValue
        self.__iterator = iterator
        self.__term1 = term1
        self.__term2 = term2
        self.__childs = childs

    # GETTERS
    def getUiID(self):
        """
        Get Expression uiID.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__uiID
    
    def getExpType(self):
        """
        Get Expression type.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__expType

    def getCoefficient(self):
        """
        Get Expression coefficient.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__coefficient
    
    def getOffset(self):
        """
        Get Expression offset.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__offset

    def getFrom(self):
        """
        Get Expression from.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__from

    def getTo(self):
        """
        Get Expression to.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__to

    def getIterator(self):
        """
        Get Expression iterator.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__iterator

    def getTerm1(self):
        """
        Get Expression term1.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        dict
        """

        return self.__term1

    def getTerm2(self):
        """
        Get Expression term2.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        dict
        """

        return self.__term2

    def getChilds(self):
        """
        Get Expression childs.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        list
        """

        return self.__childs


##################_____PUBLIC CLASSES_____##################

# PARAMETER
class Parameter:

    # CONSTRUCTOR
    def __init__(self, name: str, value: int):
        """
        Create Circuit Parameter.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Parameter name.
        value : int | str
            Parameter value.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('value', value, (int, str))
        )
        if isinstance(value, str):
            checkMathExpression('value', value)
        
        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__value = str(value)


    # GETTERS
    def getUiID(self):
        """
        Get Circuit Parameter uiID.

        Prerequisites
        ----------
        - Created parameter.

        Output
        ----------
        str
        """
        return self.__uiID

    def getName(self):
        """
        Get Circuit Parameter name.

        Prerequisites
        ----------
        - Created parameter.

        Output
        ----------
        str
        """
        return self.__name
    
    def getValue(self):
        """
        Get Circuit Parameter value.

        Prerequisites
        ----------
        - Created parameter.

        Output
        ----------
        str
        """
        return self.__value


# AUXDATA
class AuxData:
    
    # CONSTRUCTOR
    def __init__(self, name: str, value: int):
        """
        Create Circuit Auxiliary Data.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Auxiliary Data name.
        value : int | list
            Auxiliary Data value or list of values.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('value', value, (int, list))
        )
        if isinstance(value, list):
            if not value:
                raise ValueError('List of values should not be empty')

            for v in value:
                checkInputTypes(('value', v, (int,)))

        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__value = str(value)
    

    # GETTERS
    def getUiID(self):
        """
        Get Circuit Auxiliary Data uiID.

        Prerequisites
        ----------
        - Created auxiliary data.

        Output
        ----------
        str
        """
        return self.__uiID

    def getName(self):
        """
        Get Circuit Auxiliary Data name.

        Prerequisites
        ----------
        - Created auxiliary data.

        Output
        ----------
        str
        """
        return self.__name
    
    def getValue(self):
        """
        Get Circuit Auxiliary Data value.

        Prerequisites
        ----------
        - Created auxiliary data.

        Output
        ----------
        str
        """
        return self.__value
    

# CLASS
class Class:

    # CONSTRUCTOR
    def __init__(self, name: str, numberOfVars: int, description: str = ''):
        """
        Create Circuit Class.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Class name.
        numberOfVars : int | Parameter obj
            Number of Class variables.
        description : str
            Optional argument. Class description.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('numberOfVars', numberOfVars, (int, Parameter)),
            ('description', description, (str,))
        )

        self.__properties = []
        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__numberOfVars = str(numberOfVars) if isinstance(numberOfVars, int) else numberOfVars.getValue()
        self.__description = description


    # GETTERS
    def getProperties(self):
        """
        Get Circuit Class properties.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        list
        """
        return self.__properties
    
    def getUiID(self):
        """
        Get Circuit Class uiID.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        str
        """
        return self.__uiID

    def getName(self):
        """
        Get Circuit Class name.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        str
        """
        return self.__name
    
    def getNumberOfVars(self):
        """
        Get Circuit Class number of variables.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        str
        """
        return self.__numberOfVars
    
    def getDescription(self):
        """
        Get Circuit Class description.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        str
        """
        return self.__description
    

    # METHODS
    def addProperty(self, name: str, value: list):
        """
        Add Class Property.

        Prerequisites
        ----------
        - Created class.

        Parameters
        ----------
        name : str
            Class Property name.
        value : list
            List of property values. It may be the same that Class number of variables.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('value', value, (list,))
        )
        for v in value:
            checkInputTypes(('value', v, (int,)))

        if len(value) != int(self.__numberOfVars): # number of values and number of vars are not the same
            raise ValueError('Quantity of property values and number of variables must be the same')
        
        self.__properties.append({
            'uiID': str(uuid.uuid4()),
            'Name': name,
            'Values': list(map(str, value))
        })

        return self


# VARIABLE
class Variable:

    # CONSTRUCTOR
    def __init__(self, name: str, classes, description: str = ''):
        """
        Create Circuit Variable.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Variable name.
        classes : Class obj | list
            Class object or list of Class objects.
        description : str
            Optional argument. Variable description.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('classes', classes, (Class, list)),
            ('description', description, (str,))
        )

        self.__classes = []
        
        if isinstance(classes, list):
            if not classes:
                raise ValueError('List of classes should not be empty')

            for c in classes:
                checkInputTypes(('classes', c, (Class,)))

            for c in classes:
                self.__classes.append(c.getUiID())
        
        else:
            self.__classes.append(classes.getUiID())

        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__description = description

    # GETTERS
    def getClasses(self):
        """
        Get Circuit Variable Classes uiID.

        Prerequisites
        ----------
        - Created variable.

        Output
        ----------
        list
        """
        return self.__classes

    def getUiID(self):
        """
        Get Circuit Variable uiID.

        Prerequisites
        ----------
        - Created variable.

        Output
        ----------
        str
        """
        return self.__uiID
    
    def getName(self):
        """
        Get Circuit Variable name.

        Prerequisites
        ----------
        - Created variable.

        Output
        ----------
        str
        """
        return self.__name
    
    def getDescription(self):
        """
        Get Circuit Variable description.

        Prerequisites
        ----------
        - Created variable.

        Output
        ----------
        str
        """
        return self.__description


# RULE
class Rule:

    # CONSTRUCTOR
    def __init__(self, name: str, lambdaValue: int, description = '', disabled = False):
        """
        Create Circuit Rule.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Rule name.
        lambdaValue : int | str
            Parameter value.
        description : str
            Optional argument. Rule description.
        disabled : bool
            Optional argument. Enable / disable rule.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('lambdaValue', lambdaValue, (int, str)),
            ('description', description, (str,)),
            ('disabled', disabled, (bool,)),
        )
        if isinstance(lambdaValue, str):
            checkMathExpression('lambdaValue', lambdaValue)

        self.__expressions = []
        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__lambda = str(lambdaValue)
        self.__description = description
        self.__disabled = str(disabled)


    # GETTERS
    def getExpressions(self):
        """
        Get Circuit Rule expressions.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        list
        """

        return self.__expressions

    def getUiID(self):
        """
        Get Circuit Rule uiID.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__uiID
    
    def getName(self):
        """
        Get Circuit Rule name.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__name
    
    def getLambda(self):
        """
        Get Circuit Rule lambda.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__lambda
    
    def getDescription(self):
        """
        Get Circuit Rule description.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__description
    
    def getDisabled(self):
        """
        Get Circuit Rule disable status.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__disabled

    # METHODS
    def addExpression(self, expression):
        """
        Add Rule Expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        expression : SummatoryExp obj | SquaredExp obj | LinearExp obj | QuadraticExp obj | OffsetExp obj | list
            Expression to add. It could be an object or a list of following objects: SummatoryExp, SquaredExp, LinearExp, QuadraticExp or OffsetExp.
        
        Output
        ----------
        Rule obj
        """
        def appendExpression(expression):
            self.__expressions.append({
                'uiID': expression.getUiID(),
                'Type': expression.getExpType(),
                'Coefficient': expression.getCoefficient(),
                'Offset': expression.getOffset(),
                'From': expression.getFrom(),
                'To': expression.getTo(),
                'Iterator': expression.getIterator(),
                'Term1': expression.getTerm1(),
                'Term2': expression.getTerm2(),
                'Childs': expression.getChilds()
            })

        checkInputTypes(
            ('expression', expression, (SummatoryExp, SquaredExp, LinearExp, QuadraticExp, OffsetExp, list))
        )
        if isinstance(expression, list):
            if not expression:
                raise ValueError('List of expressions should not be empty')
            
            for e in expression:
                checkInputTypes(
                    ('expression', e, (SummatoryExp, SquaredExp, LinearExp, QuadraticExp, OffsetExp, list))
                )

            for e in expression:
                appendExpression(e)
        
        else:
            appendExpression(expression)

        return self


# OFFSET EXPRESSION
class OffsetExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, offset: int): 
        """
        Create Offset expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        offset : int | str
            Offset value.
        """
        checkInputTypes(
            ('offset', offset, (int, str))
        )

        super().__init__(expType='OFFSET', offset=str(offset))


# LINEAR EXPRESSION
class LinearExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, variable: tuple, coefficient: int = ''): 
        """
        Create Linear expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        variable: tuple
            Circuit variable and values. First element: Variable obj. Second element: value or list of values (One per class in variable).
        coefficient : int | str
            Optional argument. Coefficient value.
        """
        def appendIndex(term: dict, variable: Variable, index: int):
            term['Indexes'].append({
                'uiID': str(uuid.uuid4()),
                'Value': str(variable[1][index]) if isinstance(variable[1], list) else str(variable[1]),
                'ClassID': variable[0].getClasses()[index]
            })

        def checkVariablesAndClasses(variable):
            numberOfClasses = len(variable[0].getClasses())

            if isinstance(variable[1], list):
                if len(variable[1]) != numberOfClasses:
                    raise ValueError(f'Expected {numberOfClasses} variable values, not {len(variable[1])}')
                
            else:
                if numberOfClasses != 1:
                    raise ValueError(f'Expected {numberOfClasses} variable values, not 1')
        
        if isinstance(variable, tuple):
            if len(variable) != 2: # number of variable elements are not 2
                raise ValueError('variable takes 2 positional arguments')
        
        checkInputTypes(
            ('variable', variable, (tuple,)),
            ('variable', variable[0], (Variable,)),
            ('variable', variable[1], (int, str, list)),
            ('coefficient', coefficient, (int, str))
        )
        if isinstance(variable[1], list):
            for v in variable[1]:
                checkInputTypes(('variable', v, (int, str)))
        
        checkVariablesAndClasses(variable) # check number of variable numbers are the same that variable classes

        term1 = {
            'Indexes': [],
            'uiID': str(uuid.uuid4()),
            'VariableID': variable[0].getUiID()
        }

        if isinstance(variable[1], list):
            for index in range(0, len(variable[1])):
                appendIndex(term1, variable, index)
        
        else:
            appendIndex(term1, variable, 0)

        super().__init__(expType='LINEAR', coefficient=str(coefficient), term1=term1)


# QUADRATIC EXPRESSION
class QuadraticExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, variable1: tuple, variable2: tuple, coefficient: int = ''): 

        """
        Add Quadratic expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        variable1: tuple
            Circuit variable and values. First element: Variable obj. Second element: value or list of values (One per class in variable).
        variable2: tuple
            Circuit variable and values. First element: Variable obj. Second element: value or list of values (One per class in variable).
        coefficient : int | str
            Optional argument. Coefficient value.
        """
        def appendIndex(term: dict, variable: Variable, index: int):
            term['Indexes'].append({
                'uiID': str(uuid.uuid4()),
                'Value': str(variable[1][index]) if isinstance(variable[1], list) else str(variable[1]),
                'ClassID': variable[0].getClasses()[index]
            })

        def checkVariablesAndClasses(variable):
            numberOfClasses = len(variable[0].getClasses())

            if isinstance(variable[1], list):
                if len(variable[1]) != numberOfClasses:
                    raise ValueError(f'Expected {numberOfClasses} variable values, not {len(variable[1])}')
                
            else:
                if numberOfClasses != 1:
                    raise ValueError(f'Expected {numberOfClasses} variable values, not 1')

        if isinstance(variable1, tuple):
            if len(variable1) != 2: # number of variable1 elements are not 2
                raise ValueError('variable1 takes 2 positional arguments')
        if isinstance(variable2, tuple):
            if len(variable2) != 2: # number of variable2 elements are not 2
                raise ValueError('variable2 takes 2 positional arguments')
        
        checkInputTypes(
            ('variable1', variable1, (tuple,)),
            ('variable1', variable1[0], (Variable,)),
            ('variable1', variable1[1], (int, str, list)),
            ('variable2', variable2, (tuple,)),
            ('variable2', variable2[0], (Variable,)),
            ('variable2', variable2[1], (int, str, list)),
            ('coefficient', coefficient, (int, str))
        )
        if isinstance(variable1[1], list):
            for v in variable1[1]:
                checkInputTypes(('variable1', v, (int, str)))
        if isinstance(variable2[1], list):
            for v in variable2[1]:
                checkInputTypes(('variable2', v, (int, str)))

        checkVariablesAndClasses(variable1) # check number of variable numbers are the same that variable classes
        checkVariablesAndClasses(variable2)

        term1 = {
            'Indexes': [],
            'uiID': str(uuid.uuid4()),
            'VariableID': variable1[0].getUiID()
        }

        term2 = {
            'Indexes': [],
            'uiID': str(uuid.uuid4()),
            'VariableID': variable2[0].getUiID()
        }

        if isinstance(variable1[1], list):
            for index in range(0, len(variable1[1])):
                appendIndex(term1, variable1, index)
        else:
            appendIndex(term1, variable1, 0)
        
        if isinstance(variable2[1], list):
            for index in range(0, len(variable2[1])):
                appendIndex(term2, variable2, index)
        else:
            appendIndex(term2, variable2, 0)

        super().__init__(expType='QUADRATIC', coefficient=str(coefficient), term1=term1, term2=term2)


# SQUARED EXPRESSION
class SquaredExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, expression): 
        """
        Create Squared expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        expression: SummatoryExp obj | LinearExp obj | OffsetExp obj | list
            Expression or list of expressions to be squared. It could be a Summatory, Linear, or Offset expression.
        """
        childs = []
        def appendChild(expression):
            childs.append({
                'uiID': expression.getUiID(),
                'Type': expression.getExpType(),
                'Coefficient': expression.getCoefficient(),
                'Offset': expression.getOffset(),
                'From': expression.getFrom(),
                'To': expression.getTo(),
                'Iterator': expression.getIterator(),
                'Term1': expression.getTerm1(),
                'Term2': expression.getTerm2(),
                'Childs': expression.getChilds()
            })

        checkInputTypes(
            ('expression', expression, (SummatoryExp, LinearExp, OffsetExp, list))
        )
        if isinstance(expression, list):
            if not expression:
                raise ValueError('List of expressions should not be empty')
            for e in expression:
                checkInputTypes(('expression', e, (SummatoryExp, LinearExp, OffsetExp, list)))
            if isinstance(expression, list):
                for exp in expression:
                    appendChild(exp)
        
        else:
            appendChild(expression)

        super().__init__(expType='SQUARED', childs=childs)


# SUMMATORY EXPRESSION
class SummatoryExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, fromValue: int, toValue: int, expression, iterator: str = 'i'): 
        """
        Create Summatory expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        fromValue: int | str
            Start value of the summatory iteration.
        toValue: int | str
            End value of the summatory iteration.
        expression: SummatoryExp obj | SquaredExp obj | LinearExp obj | QuadraticExp obj | OffsetExp obj | list
            Expression or list of expressions to be inside of the summatory. It could be a Summatory, Squared, Linear, Quadratic or Offset expression.
        iterator: str
            Iterator name.
        """
        childs = []
        def appendChild(expression):
            childs.append({
                'uiID': expression.getUiID(),
                'Type': expression.getExpType(),
                'Coefficient': expression.getCoefficient(),
                'Offset': expression.getOffset(),
                'From': expression.getFrom(),
                'To': expression.getTo(),
                'Iterator': expression.getIterator(),
                'Term1': expression.getTerm1(),
                'Term2': expression.getTerm2(),
                'Childs': expression.getChilds()
            })

        checkInputTypes(
            ('fromValue', fromValue, (int, str)),
            ('toValue', toValue, (int, str)),
            ('expression', expression, (SummatoryExp, SquaredExp, LinearExp, QuadraticExp, OffsetExp, list)),
            ('iterator', iterator, (str,)),
        )
        if isinstance(expression, list):
            if not expression:
                raise ValueError('List of expressions should not be empty')
            for e in expression:
                checkInputTypes(
                    ('expression', e, (SummatoryExp, SquaredExp, LinearExp, QuadraticExp, OffsetExp, list))
                )
            if isinstance(expression, list):
                for exp in expression:
                    appendChild(exp)
        
        else:
            appendChild(expression)

        super().__init__(expType='SUMMATORY', fromValue=str(fromValue), toValue=str(toValue), iterator=iterator, childs=childs)