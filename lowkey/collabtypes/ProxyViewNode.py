from lowkey.collabtypes.RealViewNode import RealViewNode
from lowkey.collabtypes.ViewNode import ViewNode
from lowkey.collabtypes import Literals

class ProxyViewNode(ViewNode):
    def __init__(self):
        self._realViewNode: [RealViewNode] = []

    def addViewNode(self, node: RealViewNode):
        flag = False
        for nodes in self._realViewNode:
            if nodes.getViewNodeName() == node.getViewNodeName() or nodes.getViewNodeFeature(Literals.FOR) == node.getViewNodeFeature(Literals.FOR):
                flag = True

        if not flag:
            self._realViewNode.append(node)

    # def show(self):
