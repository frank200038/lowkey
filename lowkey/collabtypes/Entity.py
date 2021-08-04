#!/usr/bin/env python

__author__ = "Istvan David"
__copyright__ = "Copyright 2021, GEODES"
__credits__ = "Eugene Syriani"
__license__ = "GPL-3.0"

"""
Clabject with context.
"""

from .Clabject import Clabject
from .Model import Model


class Entity(Clabject):

    def __init__(self):
        super().__init__()
    
    def setModel(self, model:Model):
        self._model = model
        model.addNode(self)
    
    def getModel(self) -> Model:
        return self._model
    
    def getAssociations(self):
        return [a for a in self._model.getAssociations() if (a.getFrom() == self or a.getTo() == self)]
    
    def getAssociationsByName(self, name):
        return [a for a in self.getAssociations() if a.getName() == name]
    
    def addAssociation(self, association):
        assert association.getFrom() == self or association.getTo() == self
        self._model.addNode(association)
        
    def removeAssociation(self, association):
        assert association.getFrom() == self or association.getTo() == self
        self._model.removeNode(association)
