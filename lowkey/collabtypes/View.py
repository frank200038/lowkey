from lowkey.collabtypes.Entity import Entity
from lowkey.collabtypes.Model import Model
from lowkey.collabtypes.ProxyViewNode import ProxyViewNode
from lowkey.collabtypes.RealViewNode import RealViewNode
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes import Literals
from lowkey.lww.LWWVertex import LWWVertex
from lowkey.lww.LWWEdge import LWWEdge


class View(Model):

    def __init__(self, typedBy, model: Model, viewName, entityName, types):
        super().__init__()
        self._typedBy = typedBy
        self._model = model
        self._viewName = viewName
        self._entityName = entityName  # TODO: Change to Optional
        self._types = types

        self.__createViewGraph()


        # self._proxyViewNode: ProxyViewNode = ProxyViewNode()

    '''
    Compliance check should be enforced each clabject of each type should have unique name 
    Ex: Cannot have two mindmap that has same name or two centralTopic of the same name.
    Advantage ? Disadvantage ?
    '''

    # def _getCorrespondentClabject(self):
    #     return [clabject for clabject in self._model.getNodes() if clabject.getName() == self._entityName and
    #             clabject.getType() == self._typedBy][0]
    def getViewName(self):
        return self._viewName

    def getTypes(self):
        return self._types

    def getGraph(self):
        return self.persistence


    def getRoots(self):
        return self.persistence.getRoots()
    def getVerticesInViewByType(self, type):
        if type in self._types:
            return [a.getFeature(Literals.NODES) for a in self.persistence.getAllVertices() if
                    a.getFeature(Literals.NODES).getType() == type]
    def __createViewGraph(self):
        nodes = self.__findAllNodes()

        # TODO: Better Error handling
        if len(nodes) == 0:
            raise Exception('No nodes found for the view')

        # TODO: Change to store ID only
        # TODO: Remove Clock mechanisme after re-organizing node CRUD Operations
        for node in nodes:
            self._clock.sleepOneStep()
            vertex = LWWVertex()
            vertex.add(Literals.NODES, node, self.currentTime())

            self._clock.sleepOneStep()
            self.persistence.addVertex(vertex, self.currentTime())

            vertices = self.persistence.getAllVertexNodes()

            temp_entity = Entity(node)

            outNodes = [a for a in vertices if a in
                        list(map(lambda x: x.getFeature(Literals.ASSOCIATION_TO),
                                 temp_entity.getOutgoingAssociations()))]

            inNodes = [a for a in vertices if a in
                       list(map(lambda x: x.getFeature(Literals.ASSOCIATION_FROM),
                                temp_entity.getIncomingAssociations()))]

            for outNode in outNodes:
                name = node.getName() + "TO" + outNode.getName()


                toAddOutVertex = self.persistence.findVertexByAttr(Literals.NODES, outNode)
                if toAddOutVertex is None:
                    self._clock.sleepOneStep()
                    toAddOutVertex = LWWVertex()
                    toAddOutVertex.add(Literals.NODES, outNode, self.currentTime())

                if not self.persistence.edgeExistsWithName(name):
                    self._clock.sleepOneStep()
                    edge = LWWEdge()
                    edge.add("name", name, self.currentTime())
                    edge.add("from", vertex, self.currentTime())
                    edge.add("to", toAddOutVertex, self.currentTime())

                    self._clock.sleepOneStep()
                    self.persistence.addEdge(edge, self.currentTime())

            for inNode in inNodes:
                name = inNode.getName() + "TO" + node.getName()

                toAddInVertex = self.persistence.findVertexByAttr(Literals.NODES, inNode)
                if toAddInVertex is None:
                    self._clock.sleepOneStep()

                    toAddInVertex = LWWVertex()
                    toAddInVertex.add(Literals.NODES, inNode, self.currentTime())

                if not self.persistence.edgeExistsWithName(name):
                    self._clock.sleepOneStep()
                    edge = LWWEdge()
                    edge.add("name", name, self.currentTime())
                    edge.add("from", toAddInVertex, self.currentTime())
                    edge.add("to", vertex, self.currentTime())

                    self._clock.sleepOneStep()
                    self.persistence.addEdge(edge, self.currentTime())

    def getAdjacencyListForVertex(self, vertex):
        return self.persistence.getAdjacencyListForVertex(vertex)

    def __findAllNodes(self):
        nodes = []
        if len(self._types) != 0:
            # clabject: Clabject = self._getCorrespondentClabject()
            for type in self._types:
                for node in self._model.getNodesByType(type):
                    if node.getFeature(Literals.FOR) == self._entityName:
                        nodes.append(node)
        return nodes



