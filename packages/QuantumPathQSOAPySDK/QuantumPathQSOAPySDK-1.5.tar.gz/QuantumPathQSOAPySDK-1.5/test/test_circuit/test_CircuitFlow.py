import unittest
from QuantumPathQSOAPySDK import QSOAPlatform

##################_____CIRCUITFLOW_____##################
class Test_CircuitFlow(unittest.TestCase):

    # CIRCUIT FLOW
    def test_CircuitFlow(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        self.assertIsInstance(flow, qsoa.CircuitFlow)


##################_____GET FLOW BODY_____##################
class Test_GetFlowBody(unittest.TestCase):

    # GET FLOW BODY
    def test_getFlowBody(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        flowBody = flow.getFlowBody()

        self.assertIsInstance(flowBody, dict)
        self.assertEqual(flowBody, {'class': 'go.GraphLinksModel', 'nodeDataArray': [], 'linkDataArray': []})


##################_____GET PARSED BODY_____##################
class Test_GetParsedBody(unittest.TestCase):

    # GET PARSED BODY
    def test_getParsedBody(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        parsedBody = flow.getParsedBody()

        self.assertIsInstance(parsedBody, str)
        self.assertEqual(parsedBody, '{"class":"go.GraphLinksModel","nodeDataArray":[],"linkDataArray":[]}')


##################_____START NODE_____##################
class Test_StartNode(unittest.TestCase):

    # START NODE
    def test_startNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        startNode = flow.startNode()

        self.assertIsInstance(startNode, dict)
        self.assertEqual(startNode, {'category': 'Start', 'text': 'Start', 'key': -1, 'loc': ''})
        self.assertEqual(flow.getFlowBody(), {'class': 'go.GraphLinksModel', 'nodeDataArray': [{'category': 'Start', 'text': 'Start', 'key': -1, 'loc': ''}], 'linkDataArray': []})


##################_____INIT NODE_____##################
class Test_InitNode(unittest.TestCase):

    # INIT NODE
    def test_initNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        initNode = flow.initNode(0)

        self.assertIsInstance(initNode, dict)
        self.assertEqual(initNode, {'category': 'Init', 'text': '0', 'key': -1, 'loc': ''})
        self.assertEqual(flow.getFlowBody(), {'class': 'go.GraphLinksModel', 'nodeDataArray': [{'category': 'Init', 'text': '0', 'key': -1, 'loc': ''}], 'linkDataArray': []})
    
    # BAD ARGUMENT TYPE startValue
    def test_initNode_badArgumentType_startValue(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        try:
            flow.initNode('startValue')

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CIRCUIT NODE_____##################
class Test_CircuitNode(unittest.TestCase):

    # CIRCUIT NODE
    def test_circuitNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        circuitNode = flow.circuitNode('circuitName')

        self.assertIsInstance(circuitNode, dict)
        self.assertEqual(circuitNode, {'category': 'Circuit', 'text': 'circuitName', 'key': -1, 'loc': ''})
        self.assertEqual(flow.getFlowBody(), {'class': 'go.GraphLinksModel', 'nodeDataArray': [{'category': 'Circuit', 'text': 'circuitName', 'key': -1, 'loc': ''}], 'linkDataArray': []})
    
    # BAD ARGUMENT TYPE circuitName
    def test_circuitNode_badArgumentType_circuitName(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        try:
            flow.circuitNode(99)

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____REPEAT NODE_____##################
class Test_RepeatNode(unittest.TestCase):

    # REPEAT NODE
    def test_repeatNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        repeatNode = flow.repeatNode(1000)

        self.assertIsInstance(repeatNode, dict)
        self.assertEqual(repeatNode, {'category': 'Repeat', 'text': '1000', 'key': -1, 'loc': ''})
        self.assertEqual(flow.getFlowBody(), {'class': 'go.GraphLinksModel', 'nodeDataArray': [{'category': 'Repeat', 'text': '1000', 'key': -1, 'loc': ''}], 'linkDataArray': []})
    
    # BAD ARGUMENT TYPE numReps
    def test_repeatNode_badArgumentType_numReps(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        try:
            flow.repeatNode('numReps')

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____END NODE_____##################
class Test_EndNode(unittest.TestCase):

    # END NODE
    def test_endNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        endNode = flow.endNode()

        self.assertIsInstance(endNode, dict)
        self.assertEqual(endNode, {'category': 'End', 'text': 'End', 'key': -1, 'loc': ''})
        self.assertEqual(flow.getFlowBody(), {'class': 'go.GraphLinksModel', 'nodeDataArray': [{'category': 'End', 'text': 'End', 'key': -1, 'loc': ''}], 'linkDataArray': []})


##################_____COMMENT NODE_____##################
class Test_CommentNode(unittest.TestCase):

    # COMMENT NODE
    def test_commentNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        commentNode = flow.commentNode('comment')

        self.assertIsInstance(commentNode, dict)
        self.assertEqual(commentNode, {'category': 'Comment', 'text': 'comment', 'key': -1, 'loc': ''})
        self.assertEqual(flow.getFlowBody(), {'class': 'go.GraphLinksModel', 'nodeDataArray': [{'category': 'Comment', 'text': 'comment', 'key': -1, 'loc': ''}], 'linkDataArray': []})
    
    # BAD ARGUMENT TYPE numReps
    def test_commentNode_badArgumentType_numReps(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()

        try:
            flow.commentNode(99)

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____LINK NODES_____##################
class Test_LinkNodes(unittest.TestCase):

    # LINK NODES
    def test_linkNodes(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()
        fromNode = flow.startNode()
        toNode = flow.startNode()

        link = flow.linkNodes(fromNode, toNode)

        self.assertIsInstance(link, dict)
        self.assertEqual(link, {'from': -1, 'to': -2, 'points': []})
        self.assertEqual(flow.getFlowBody(), {'class': 'go.GraphLinksModel', 'nodeDataArray': [{'category': 'Start', 'text': 'Start', 'key': -1, 'loc': ''}, {'category': 'Start', 'text': 'Start', 'key': -2, 'loc': ''}], 'linkDataArray': [{'from': -1, 'to': -2, 'points': []}]})
    
    # BAD ARGUMENT TYPE fromNode
    def test_linkNodes_badArgumentType_fromNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()
        toNode = flow.startNode()

        try:
            flow.linkNodes(99, toNode)

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE toNode
    def test_linkNodes_badArgumentType_toNode(self):
        qsoa = QSOAPlatform()
        flow = qsoa.CircuitFlow()
        fromNode = flow.startNode()

        try:
            flow.linkNodes(fromNode, 99)

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()