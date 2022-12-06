from lowkey.collabtypes.Model import Model


class ViewPoint(Model):
    """
    ViewPoint establishes the conventions for constructing, interpreting and analysing the view to address concerns
    framed by that viewpoint (Multi-view approcahes for software and system modelling: A systematic literature review, Antonio Cicchetti, 2019)

    ViewPoint govers a view, thus a viewpoint can be reused by multiple views to be applied on different entities.

    By default, contains all nodes from the model that conforms to the specified type
    """
    def __init__(self, typedBy, model: Model, viewPointName, types):
        super().__init__()
        self._typedBy = typedBy
        self._model = model
        self._viewPointName = viewPointName
        self._types = types
        self._flag = 0 # If the specified types have modified or not. 0 = unchanged/extended -1 = types removed

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

    def getViewPointName(self):
        return self._viewPointName

    def getFlag(self):
        return self._flag

    def restoreFlag(self):
        self._flag = 0

    def _updateType(self, types):
        """
        Updates the types specified by the ViewPoint.
        If types are extended (added), flag will remain unchanged
        However, if types are removed, flag will be set to -1 to indicate some types are removed from the existing types

        :param types: New Types of the ViewPoint
        """
        current_types = self._types.copy()

        deleted = False

        for type in current_types:
            if type not in types:
                deleted = True
                break

        self._flag = -1 if deleted else 0

        self._types = types
    def __findAllNodes(self):
        """
        Returns all nodes of the model that are of the specified type. SuperType is supported as well.

        :return: List of nodes of the model that are of the specified type
        """
        nodes_list = []
        if len(self._types) != 0:
            for type in self._types:
                nodes = self._model.getNodesByType(type)
                if len(nodes) != 0:
                    nodes_list.extend(nodes)
                else:
                    nodes = self._model.getNodesBySuperType(type)
                    if len(nodes) != 0:
                        nodes_list.extend(nodes)
                    else:
                        continue
        return nodes_list
