#!/usr/bin/env python
import logging
import uuid

from metamodel.entities.MindMapModel import MindMapModel

from editor import MindMapPackage
from lowkey.collabtypes.Clabject import Clabject
from metamodel.entities.CentralTopic import CentralTopic
from metamodel.entities.MainTopic import MainTopic
from metamodel.entities.MindMap import MindMap
from metamodel.entities.SubTopic import SubTopic


__author__ = "Istvan David"
__copyright__ = "Copyright 2021, GEODES"
__credits__ = "Eugene Syriani"
__license__ = "GPL-3.0"

"""
Session object to manage local modeling data.
"""


class EditorSession():
    
    def __init__(self):
        self._id = uuid.uuid1()
        self._mindmapmodel = MindMapModel()
        self._mindmap = MindMap()
        self._mindmap.addToModel(self._mindmapmodel)
        self._tmp = []
    
    def classFactory(self, classname):
        if classname.lower() not in [k.lower() for k in globals().keys()]:
            return None
        klass = {k.lower():v for k, v in globals().items()}[classname.lower()]
        return klass()
    
    def integrateEntity(self, entity):
        logging.debug(entity)
        logging.debug(" Integrating entity {} ({})'.".format(entity.getName(), entity.getType()))
        if(isinstance(entity, CentralTopic)):
            logging.debug(">>integrating as centraltopic")
            entity.addToModel(self._mindmapmodel)
            self._mindmap.setTopic(entity)
        elif(isinstance(entity, MainTopic)):
            logging.debug(">>integrating as maintopic")
            entity.addToModel(self._mindmapmodel)
            centralTopic = self._mindmap.getTopic()
            centralTopic.addMainTopic(entity)
        elif(isinstance(entity, SubTopic)):
            logging.debug(">>integrating as subtopic")
            entity.addToModel(self._mindmapmodel)
            self._tmp.append(entity)
            print(self._tmp)
            logging.debug("entity added to _tmp")
        else:
            logging.debug("Unexpected type")
            
    def integrateAssociation(self, association):
        logging.debug(association)
        associationName = association.getName()
        fromEntity = association.getFrom()
        toEntity = association.getTo()
        logging.debug(" Integrating association '{}' between {} and {}.".format(associationName, fromEntity, toEntity))
        
        print(self._tmp)
        
        st = None
        
        for e in self._tmp:
            print("printing e")
            print(e)
            print(e.getName())
            print(toEntity)
            if e.getName() == toEntity:
                st = e
                break
        
        print(st)
        
        ct = self._mindmap.getTopic()
        for mt in ct.getMainTopics():
            if mt.getName() == fromEntity:
                mt.addSubTopic(st)
                self._tmp.remove(st)