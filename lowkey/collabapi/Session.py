#!/usr/bin/env python
import logging
import uuid
import re

from lowkey.collabtypes import Literals
from lowkey.collabtypes.View import View
from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from .Parser import Parser

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
        node.addToModel(self.getModels()[0])

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

    def createView(self, params):
        _, typedBy = params[0]
        _, entityName = params[1]
        _, viewName = params[2]
        _, typesOriginal = params[3]

        types = re.findall(r'\{(.*?)\}', typesOriginal)[0].split(',')

        # TODO: Same as mentionned above. Potentially a change.
        for model in self.getModels():
            print(model.getType())

        linkedModel = self.getModels()[0]
        print(linkedModel)

        print(linkedModel.getNodes())

        createdView = View(typedBy=typedBy, model=linkedModel, viewName=viewName,entityName=entityName, types=types)
        createdView.createProxyViewNode()
        linkedModel.appendView(createdView)
