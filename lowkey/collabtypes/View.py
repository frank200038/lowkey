from lowkey.collabtypes.Entity import Entity
from lowkey.collabtypes.Model import Model
from lowkey.collabtypes.ProxyViewNode import ProxyViewNode
from lowkey.collabtypes.RealViewNode import RealViewNode
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes import Literals
from lowkey.lww.LWWVertex import LWWVertex
from lowkey.lww.LWWEdge import LWWEdge
from lowkey.collabtypes.ViewPoint import ViewPoint

class View(Model):

    def __init__(self, viewPoint : ViewPoint, entityName, viewName):
        super().__init__()
        self._viewPoint = viewPoint
        self._entityName = entityName
        self._viewName = viewName

        self._nodes = self.__filterNodes()
        self.__createViewGraph()

    '''
    Compliance check should be enforced each clabject of each type should have unique name
    Ex: Cannot have two mindmap that has same name or two centralTopic of the same name.
    Advantage ? Disadvantage ?
    '''
    def getViewName(self):
        return self._viewName

    def getTypes(self):
        return self._types

    def getGraph(self):
        return self.persistence

    def getRoots(self):
        return self.persistence.getRoots()

    def getAdjacencyListForVertex(self, vertex):
        return self.persistence.getAdjacencyListForVertex(vertex)

    def __filterNodes(self):
        def __filterNodesRec(node):
            nodeAssocitation = [a for a in associations if a.getFrom() == node]
            for n in nodeAssocitation:
                next_node = n.getTo()
                name = next_node.getName()
                if next_node in allNodes:
                    filteredNodes.append(next_node)
                __filterNodesRec(n.getTo())

        filteredNodes = []
        allNodes = self._viewPoint.getAllNodes()
        roots = [root for root in self._viewPoint.getModelRoots() if root.getName() == self._entityName]
        associations = self._viewPoint.getAssociations()

        nodesFromRoots = [a.getTo() for a in associations if a.getFrom() in roots]

        for node in nodesFromRoots:
            name = node.getName()
            if node in allNodes:
                filteredNodes.append(node)
            __filterNodesRec(node)

        return filteredNodes

    def __outAndInAssociationFromNodeVertices(self,vertices, node):
        temp_entity = Entity(node)
        outNodes = [a for a in vertices if a in
                    list(map(lambda x: x.getFeature(Literals.ASSOCIATION_TO),
                             temp_entity.getOutgoingAssociations()))]

        inNodes = [a for a in vertices if a in
                   list(map(lambda x: x.getFeature(Literals.ASSOCIATION_FROM),
                            temp_entity.getIncomingAssociations()))]

        return (outNodes, inNodes)

    def __addEdge(self, name, fromNode, toNode):
        self._clock.sleepOneStep()
        edge = LWWEdge()
        edge.add("name", name, self.currentTime())
        edge.add("from", fromNode, self.currentTime())
        edge.add("to", toNode, self.currentTime())

        self.persistence.addEdge(edge, self.currentTime())

        return edge

    def __addVertex(self, node):
        self._clock.sleepOneStep()
        vertex = LWWVertex()
        vertex.add(Literals.NODES, node, self.currentTime())

        self._clock.sleepOneStep()
        self.persistence.addVertex(vertex, self.currentTime())

        return vertex

    def __createViewGraph(self):
        nodes = self._nodes

        # TODO: Better Error handling
        if len(nodes) == 0:
            raise Exception('No nodes found for the view')

        # TODO: Change to store ID only
        # TODO: Remove Clock mechanisme after re-organizing node CRUD Operations
        for node in nodes:
            vertex = self.__addVertex(node)

            vertices = self.persistence.getAllVertexNodes()

            outNodes, inNodes = self.__outAndInAssociationFromNodeVertices(vertices, node)

            for outNode in outNodes:
                name = node.getName() + "TO" + outNode.getName()

                toAddOutVertex = self.persistence.findVertexByAttr(Literals.NODES, outNode)
                if toAddOutVertex is None:
                    self.__addVertex(outNode)

                if not self.persistence.edgeExistsWithName(name):
                    self.__addEdge(name, vertex, toAddOutVertex)

            for inNode in inNodes:
                name = inNode.getName() + "TO" + node.getName()

                toAddInVertex = self.persistence.findVertexByAttr(Literals.NODES, inNode)
                if toAddInVertex is None:
                    self.__addVertex(inNode)

                if not self.persistence.edgeExistsWithName(name):
                    self.__addEdge(name, toAddInVertex, vertex)


