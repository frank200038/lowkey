from lowkey.collabtypes.Entity import Entity
from lowkey.collabtypes.Model import Model
from lowkey.collabtypes.ProxyViewNode import ProxyViewNode
from lowkey.collabtypes.RealViewNode import RealViewNode
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes import Literals

class View(Model):

    def __init__(self, typedBy, model: Model, viewName, entityName, types):
        super().__init__()
        self._typedBy = typedBy
        self._model = model
        self._viewName = viewName
        self._entityName = entityName
        self._types = types
        self._proxyViewNode: ProxyViewNode = ProxyViewNode()

    '''
    Compliance check should be enforced each clabject of each type should have unique name 
    Ex: Cannot have two mindmap that has same name or two centralTopic of the same name.
    Advantage ? Disadvantage ?
    '''
    # def _getCorrespondentClabject(self):
    #     return [clabject for clabject in self._model.getNodes() if clabject.getName() == self._entityName and
    #             clabject.getType() == self._typedBy][0]
    def createProxyViewNode(self):
        nodes = []
        if len(self._types) != 0:
            # clabject: Clabject = self._getCorrespondentClabject()
            for type in self._types:
                for node in self._model.getNodesByType(type):
                    if node.getFeature(Literals.FOR) == self._entityName:
                        nodes.append(node)

        for node in nodes:
            self._proxyViewNode.addViewNode(RealViewNode(node=node))



