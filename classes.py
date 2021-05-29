from enum import Enum
from abc import ABCMeta, abstractmethod

class indicators(Enum):
    NOTHING = 0

class lines(Enum):
    NOLINE = 0
    SINGLELINE = 1
    DOUBLELINE = 2

class modes(Enum):
    NOMODE = 0
    INT_FLOAT = 1
    INT_FLOAT_FLOAT = 2
    INT_INT_INT_INT = 3

class parameters(Enum):
    THERMAL_CONDUCTIVITY = 0
    HEAT_SOURCE = 1

class sizes(Enum):
    NODES = 0
    ELEMENTS = 1
    DIRICHLET = 2
    NEUMANN = 3

class Item:
    def setId(self, id):
        self._id = id
    
    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y
    
    def setNode1(self, nodo1):
        self._nodo1 = nodo1

    def setNode2(self, nodo2):
        self._nodo2 = nodo2
    
    def setNode3(self, nodo3):
        self._nodo3 = nodo3
    
    def setValue(self, valores):
        self._valores = valores
    
    def getId(self):
        return self._id
    
    def getX(self):
        return self._x
    
    def getY(self):
        return self._y
    
    def getNode1(self):
        return self._nodo1
    
    def getNode2(self):
        return self._nodo2
    
    def getNode3(self):
        return self._nodo3
    
    def getValue(self):
        return self._valores
    
    @abstractmethod
    def setValues(self, a, b, c, d, e, f, g):
        pass

class node(Item):
    def setValues(self, a, b, c, d, e, f, g):
        self._id = a
        self._x = b
        self._y = c

class element(Item):
    def setValues(self, a, b, c, d, e, f, g):
        self._id = a
        self._nodo1 = d
        self._nodo2 = e
        self._nodo3 = f

class condition(Item):
    def setValues(self, a, b, c, d, e, f, g):
        self._nodo1 = d
        self._valores = g

class mesh:
    parameters = [2]
    sizes = [4]

    def setParameters(self, k, Q):
        self.parameters.insert(parameters.THERMAL_CONDUCTIVITY.value,k)
        self.parameters.insert(parameters.HEAT_SOURCE.value,Q)
    
    def setSizes(self, nnodes, neltos, ndirich, nneu):
        self.sizes.insert(sizes.NODES.value, nnodes)
        self.sizes.insert(sizes.ELEMENTS.value, neltos)
        self.sizes.insert(sizes.DIRICHLET.value, ndirich)
        self.sizes.insert(sizes.NEUMANN.value, nneu)
    
    def getSize(self, s):
        return self.sizes[s]
    
    def getParameter(self, p):
        return self.parameters[p]
    
    def createData(self):
        self.node_list = []
        self.element_list = []
        self.indices_dirich = []
        self.dirichlet_list = []
        self.neuman_list = []
    
    def getNodes(self):
        return self.node_list
    
    def getElements(self):
        return self.element_list
    
    def getDirichletIndices(self):
        return self.indices_dirich
    
    def getDirichlet(self):
        return self.dirichlet_list
    
    def getNeumann(self):
        return self.neuman_list
    
    def getNode(self, i):
        return self.node_list[i]
    
    def getElement(self, i):
        return self.element_list[i]
    
    def getCondition(self, i, type):
        if type == sizes.DIRICHLET.value : return self.dirichlet_list[i]
        else : return self.neuman_list[i]