from lowkey.collabtypes.Entity import Entity
from lowkey.collabtypes.Model import Model
from lowkey.collabtypes.ProxyViewNode import ProxyViewNode
from lowkey.collabtypes.RealViewNode import RealViewNode
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes import Literals
from lowkey.lww.LWWVertex import LWWVertex
from lowkey.lww.LWWEdge import LWWEdge

class ViewPoint(Model):

    def __init__(self, typedBy, model: Model, viewPointName, types):
        super().__init__()
        self._typedBy = typedBy
        self._model = model
        self._viewPointName = viewPointName
        self._types = types

    def getTypes(self):
        return self._types

    def getViewPointName(self):
        return self._viewPointName

    def getAllNodes(self):
        return self.__findAllNodes()

    def getModelRoots(self):
        return [c for c in self._model.getClabjects() if c.getType() == self._typedBy]

    def getAssociations(self):
        return self._model.getAssociations()

    def __findAllNodes(self):
        nodes = []
        if len(self._types) != 0:
            for type in self._types:
                for node in self._model.getNodesByType(type):
                        nodes.append(node)
        return nodes
