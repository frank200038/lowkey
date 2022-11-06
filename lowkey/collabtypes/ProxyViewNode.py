from lowkey.collabtypes.Entity import Entity
from lowkey.collabtypes.RealViewNode import RealViewNode
from lowkey.collabtypes.ViewNode import ViewNode
from lowkey.collabtypes import Literals, Node
# import networkx as nx


class ProxyViewNode(ViewNode):

    def setTypeOrder(self, order):
        self._typeOrder = order

    def addAttributeNode(self, attribute, default):
        dict = {attribute: default}
        if attribute != "":
            for node in self._graphAssociation.nodes:
                nx.set_node_attributes(self._graphAssociation, {node: dict})

    def __init__(self):
        # self._toAddNodes: [RealViewNode] = []
        self._typeOrder = []
        self._graphAssociation = nx.MultiDiGraph()

    def organizeAssociations(self, node: RealViewNode):

        self._graphAssociation.add_node(node)
        self._graphAssociation.neighbors(node)
        realNode = node.getViewNode()
        entity_temp = Entity(realNode)

        list_viewNode = list(self._graphAssociation.nodes)

        outNodes = [a for a in list_viewNode if a.getViewNode() in
                    list(map(lambda x: x.getFeature(Literals.ASSOCIATION_TO), entity_temp.getOutgoingAssociations()))]
        inNodes = [a for a in list_viewNode if a.getViewNode() in
                   list(map(lambda x: x.getFeature(Literals.ASSOCIATION_FROM), entity_temp.getIncomingAssociations()))]

        # outNodes = [a for a in
        #             list(map(lambda x: x.getFeature(Literals.ASSOCIATION_TO), entity_temp.getOutgoingAssociations())) if
        #             a in list_viewNode]
        # inNodes = [a for a in
        #            list(map(lambda x: x.getFeature(Literals.ASSOCIATION_FROM), entity_temp.getIncomingAssociations()))
        #            if a in list_viewNode]

        for outNode in outNodes:
            self._graphAssociation.add_edge(node, outNode)

        for inNode in inNodes:
            self._graphAssociation.add_edge(inNode, node)

        # self.addAttributeNode("visited", False)
        nx.set_node_attributes(self._graphAssociation, {node: {"visited": False}})

    def addViewNode(self, node: Node):
        viewNode = RealViewNode(node=node)
        self.organizeAssociations(viewNode)

    # def show(self):
    #     if len(self._typeOrder) != 0:

    # def show(self):
