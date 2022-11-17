#!/usr/bin/env python
import logging
import uuid
import re

from lowkey.collabtypes import Literals
from lowkey.collabtypes.View import View
from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from .Parser import Parser
from lowkey.collabtypes.ViewPoint import ViewPoint

__author__ = "Istvan David"
__copyright__ = "Copyright 2021, GEODES"
__credits__ = "Eugene Syriani"
__license__ = "GPL-3.0"

"""
TODO: Add description
"""


class Session():

    def __init__(self):
        self._id = uuid.uuid1()
        self._parser = Parser()
        self._models = []

    def addModel(self, model):
        self._models.append(model)

    def getModels(self):
        return self._models

    def getModelById(self, id):
        return next(m for m in self.getModels() if m.getId() == id)

    def processMessage(self, message):
        command = self._parser.parseMessage(message)
        command.execute(self)

    def integrateNode(self, node):
        # TODO: Do I need to add view as a node ?
        node.addToModel(self.getModels()[0])

        views = self.getModels()[0].returnViewWithType(node.getType())
        for view in views:
            view.addNewNode(node)


    def integrateAssociation(self, params):
        association = Association()

        assert next(p for p in params if p[0] == Literals.ASSOCIATION_FROM)
        assert next(p for p in params if p[0] == Literals.ASSOCIATION_TO)
        assert next(p for p in params if p[0] == Literals.NAME)

        for param in params:
            pName = param[0]
            pValue = param[1]
            logging.debug("Executing command 'assocation.setFeature({}, {})'.".format(pName, pValue))

            # TODO : Maybe require a change (In case of multiple model value) ???
            # TODO: Enforce check. No association with different entity (Addition of FOR keyword)
            if pName == Literals.ASSOCIATION_FROM:
                fromClabject = self.getModels()[0].getNodeByName(pValue)
                association.setFrom(fromClabject)
            if pName == Literals.ASSOCIATION_TO:
                toClabject = self.getModels()[0].getNodeByName(pValue)
                association.setTo(toClabject)
            if pName == Literals.NAME:
                association.setName(pValue)
            if pName == Literals.FOR:
                association.setFor(pValue)

        self.integrateNode(association)

        toNode = association.getFeature(Literals.ASSOCIATION_TO)
        fromNode = association.getFeature(Literals.ASSOCIATION_FROM)


        views = self.getModels()[0].returnViewWithType(fromNode.getType(), toNode.getType())
        for view in views:
            view.addNewAssociation(toNode, fromNode)


    def createViewPoint(self, params):
        _, typedBy = params[0]
        _, viewPointName = params[1]
        _, typesOriginal = params[2]

        types = re.findall(r'\{(.*?)\}', typesOriginal)[0].split(',')

        linkedModel = self.getModels()[0]
        createdViewPoint = ViewPoint(typedBy=typedBy, model=linkedModel, viewPointName=viewPointName, types=types)
        linkedModel.appendViewPoint(createdViewPoint)

    def applyView(self, params):
        _, viewName = params[0]
        _, entityName = params[1]
        _, viewPointName = params[2]

        viewPoint = self.getModels()[0].getViewPointByName(viewPointName)
        createdView = View(viewPoint=viewPoint, entityName=entityName, viewName=viewName)
        self.getModels()[0].appendView(createdView)

