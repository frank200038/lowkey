from lowkey.collabtypes.Node import Node
from lowkey.collabtypes.ViewNode import ViewNode
import uuid

class RealViewNode(ViewNode):
    def __init__(self, node: Node):
        self._node = node

    def getViewNodeName(self):
        return self._node.getName()

    def getViewNodeFeature(self, feature):
        return self._node.getFeature(feature)
    # def show(self):

