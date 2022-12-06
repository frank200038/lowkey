from lowkey.collabtypes.Entity import Entity
from lowkey.collabtypes.Model import Model
from lowkey.collabtypes import Literals
from lowkey.lww.LWWVertex import LWWVertex
from lowkey.lww.LWWEdge import LWWEdge
from lowkey.lww.LWWGraph import LWWGraph
from lowkey.collabtypes.ViewPoint import ViewPoint

class View(Model):
    """
    Create a view of the model, governed by a correspondent ViewPoint that indicates which types of nodes should be included.
    (A subset of elements contained in the model)

    View apply directly on an instance (Ex: Shop, Mindmap). Once created, view is updated everytime when the user requests to display the view

    Persisted as an LWWGraph. Nodes are persisted as LWWVertex, and edges as LWWEdge.
    """
    def __init__(self, viewPoint : ViewPoint, entityName, viewName):
        super().__init__()
        self._viewPoint = viewPoint
        self._entityName = entityName
        self._viewName = viewName

        self._nodes = self.__filterNodes()
        self.__createViewGraph(self._nodes)

    '''
    Compliance check should be enforced each clabject of each type should have unique name
    Ex: Cannot have two mindmap that has same name or two centralTopic of the same name.
    Advantage ? Disadvantage ?
    '''
    def getViewName(self):
        return self._viewName

    def getTypes(self):
        return self._viewPoint.getTypes()

    def getGraph(self):
        return self.persistence

    def getRoots(self):
        return self.persistence.getRoots()

    def getViewPointName(self):
        return self._viewPoint.getViewPointName()

    def getAdjacencyListForVertex(self, vertex):
        return self.persistence.getAdjacencyListForVertex(vertex)

    def addNewNode(self, node):
        """
        Add a new node to the view (Used for updating the view)

        :param node: node to be added
        """
        toAddNode = self.persistence.findVertexByAttr(Literals.NODES, node)
        if toAddNode is None:
            self.__addVertex(node)

    def addNewAssociation(self, toNode, fromNode):
        """
        Add a new association to the view (Used for updating the view)

        :param toNode: Node where the association is pointing to
        :param fromNode: Node where the association is pointing from
        """
        name = fromNode.getName() + "TO" + toNode.getName()

        fromVertex = self.persistence.findVertexByAttr(Literals.NODES, fromNode)
        toVertex = self.persistence.findVertexByAttr(Literals.NODES, toNode)

        if not self.persistence.edgeExistsWithName(name):
            self.__addEdge(name, fromVertex, toVertex)

    def update(self):
        """
        Update the view by adding new nodes and associations, or construct new graphs if certain types are removed from ViewPoint

        Due to the same reason as to why DELETE is not implemented, if types are removed from the ViewPoint,
        a new graph will be simply constructed from the scratch
        """

        flag = self._viewPoint.getFlag()
        newNodes = []

        if flag == 0: # Types unmodified or extended
            originalNodes = self._nodes.copy()
            self._nodes = self.__filterNodes()

            newNodes = [node for node in self._nodes if node not in originalNodes]

        elif flag < 0: # Types removed from the ViewPoint

            # Reconstruct the Graph from scratch
            self.persistence = LWWGraph()
            self._nodes = newNodes = self.__filterNodes()

        if len(newNodes) != 0:
            self.__createViewGraph(newNodes)

        self._viewPoint.restoreFlag()
    def __filterNodes(self):
        """
        Filter nodes that only belongs to the entity specified in the View

        :return: List of nodes that belongs to the entity
        """
        def __filterNodesRec(node):
            """
            Recursively filter nodes

            :param node: node to be recursively filtered
            """
            nodeAssocitation = [a for a in associations if a.getFrom() == node] # Get all associations that has the node as the from node
            for n in nodeAssocitation:
                next_node = n.getTo()
                if next_node in allNodes: # If the current node is indeed present among all nodes having conformed types
                    filteredNodes.append(next_node) # Add the node to the filtered nodes
                __filterNodesRec(n.getTo()) # Otherwise, go to the next node and repeat the process

        filteredNodes = []
        allNodes = self._viewPoint.getAllNodes() # All nodes from the model that conforms to the type specified in the ViewPoint
        roots = [root for root in self._viewPoint.getModelRoots() if root.getName() == self._entityName] # Get the root of the entity on which the view is applied

        if len(roots) == 0:
            raise Exception("Entity not found")

        associations = self._viewPoint.getAssociations() # Get all associations present in the model (To be filtered)

        nodesFromRoots = [a.getTo() for a in associations if a.getFrom() in roots] # Filter the associations that stem from the roots

        for node in nodesFromRoots:
            if node in allNodes:
                filteredNodes.append(node)
            __filterNodesRec(node)

        return filteredNodes

    def __outAndInAssociationFromNodeVertices(self, vertices_node, node):
        """
        Interal auxiliary function to facilite the search of associations that has one end linked to a node already present in the graph

        :param vertices_node: List of nodes that are encapsulated in vertices
        :param node: Node to be searched
        :return: List of associations that has one end linked to (or from) a node already present in the graph
        """
        temp_entity = Entity(node) # To acheieve easily all the associations linked with the node

        # Nodes that are present in the graph and are connecting FROM the node
        outNodes = [a for a in vertices_node if a in
                    list(map(lambda x: x.getFeature(Literals.ASSOCIATION_TO),
                             temp_entity.getOutgoingAssociations()))]

        # Nodes that are present in the graph and are connecting TO the node
        inNodes = [a for a in vertices_node if a in
                   list(map(lambda x: x.getFeature(Literals.ASSOCIATION_FROM),
                            temp_entity.getIncomingAssociations()))]

        return (outNodes, inNodes)


    def __addEdge(self, name, fromNode, toNode):
        """
                Internal helper Method: Add Edge to the graph

                :param name: Name of the edge
                :param fromNode: Node from which the edge is coming from
                :param toNode: Node to which the edge is going to
                :return: Added edge
        """
        self._clock.sleepOneStep()
        edge = LWWEdge()
        edge.add("name", name, self.currentTime())
        edge.add("from", fromNode, self.currentTime())
        edge.add("to", toNode, self.currentTime())

        self.persistence.addEdge(edge, self.currentTime())

        return edge

    def __addVertex(self, node):
        """
        Internal helper Method: Add Vertex to the graph

        :param node: Node to be encapsulated in the vertex
        :return: Added vertex
        """
        self._clock.sleepOneStep()
        vertex = LWWVertex()
        vertex.add(Literals.NODES, node, self.currentTime())

        self._clock.sleepOneStep()
        self.persistence.addVertex(vertex, self.currentTime())

        return vertex

    def __createViewGraph(self, nodes=[]):
        """
        Internal Methode: Create graph that contains nodes that belong to the entity and conform to the type specified in the ViewPoint

        Nodes and associations are persisted as LWWVertex and LWWEdge respectively

        :param nodes: List of nodes to be added to the graph
        """

        if len(nodes) == 0:
            print("No nodes found for the entity for now")
            return

        for node in nodes:
            vertex = self.__addVertex(node)

            verticies_node = self.persistence.getAllVertexNodes()

            outNodes, inNodes = self.__outAndInAssociationFromNodeVertices(verticies_node, node)

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


