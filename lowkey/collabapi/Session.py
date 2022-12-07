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


    def createViewPoint(self, params):
        """
        Create a view point with a given name and types

        :param params: transmited parameters containing the name of the view point and the types, and the type of model
        """
        _, typedBy = params[0]
        _, viewPointName = params[1]
        _, typesOriginal = params[2]

        if self.__findViewPoint(viewPointName):
            print("ViewPoint {} already exists".format(viewPointName))
            return
        else:
            types = re.findall(r'\{(.*?)\}', typesOriginal)[0].split(',') # Regex to seperate types enclosed in {}

            linkedModel = self.getModels()[0]
            createdViewPoint = ViewPoint(typedBy=typedBy, model=linkedModel, viewPointName=viewPointName, types=types)
            linkedModel.appendViewPoint(createdViewPoint)

    def applyView(self, params):
        """
        Create a view that acts on a specific entity and governed by a given view point

        :param params: transmited parameters containing the name of the view, the name of the view point and the name of the entity
        """
        _, viewName = params[0]
        _, entityName = params[1]
        _, viewPointName = params[2]

        # Error handling: View cannot be created if the view name already exists, or if the view point does not exist, or if the entity does not exist
        if self.__findView(viewName):
            print("View {} already exists".format(viewName))
            return
        else:
            viewPoint = self.__findViewPoint(viewPointName)

            if viewPoint is not None:
                try:
                    createdView = View(viewPoint=viewPoint, entityName=entityName, viewName=viewName)
                    self.getModels()[0].appendView(createdView)
                except Exception as e:
                    print("Error on applying View. {}".format(e))
            else:
                print("ViewPoint {} not found".format(viewPointName))
                return
    def updateViewPointType(self, params):
        """
        Responsible for updating the types specified in a given view point

        :param params: Transmited parameters containing the name of the view point and the new types to be updated
        """
        _, viewPointName = params[0]
        _, typesOriginal = params[1]

        types = re.findall(r'\{(.*?)\}', typesOriginal)[0].split(',')  # Regex to seperate types enclosed in {}

        viewPoint = self.__findViewPoint(viewPointName)

        if viewPoint is not None:
           viewPoint._updateType(types)
        else:
            print("View Point does not exist")


    def __findViewPoint(self, viewPointName):
        """
        Find a view point by its name

        :param viewPointName: Name of the view point to be found
        :return: the view point if found, None otherwise
        """
        linkedModel = self.getModels()[0]
        viewPoint = linkedModel.getViewPointByName(viewPointName)
        return viewPoint

    def __findView(self, viewName):
        """
        Find a view by its name

        :param viewName: name of the view to be found
        :return: view if found, None otherwise
        """
        linkedModel = self.getModels()[0]
        view = linkedModel.getViewByName(viewName)
        return view


