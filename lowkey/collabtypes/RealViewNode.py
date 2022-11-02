import lowkey.lww.LWWMap as LWW

from lowkey.collabtypes.Node import Node
from lowkey.collabtypes.ViewNode import ViewNode
import uuid


class RealViewNode(ViewNode):
    def __init__(self, node: Node):
        self._node = node

    def getViewNode(self):
        return self._node

    # def show(self):
