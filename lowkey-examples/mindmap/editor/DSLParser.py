#!/usr/bin/env python
import logging
import os
import sys

from lowkey.collabapi.commands.CreateClabjectCommand import CreateClabjectCommand
from lowkey.collabtypes import Literals

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from editor.commands.ReadCommand import ReadCommand
from editor.commands.ReadObjectsCommand import ReadObjectsCommand

from metamodel import MindMapPackage

__author__ = "Istvan David"
__copyright__ = "Copyright 2021, GEODES"
__credits__ = "Eugene Syriani"
__license__ = "GPL-3.0"

"""TODO: Description goes here.
"""


class DSLParser():
    
    _globalCommands = ["CREATE-VIEW","CREATE", "LINK", "UPDATE", "DELETE"]
    _localCommands = ["READ", "OBJECTS"]
    
    def tokenize(self, message):
        return message.split()
    
    def isGlobalCommand(self, command):
        return command.upper() in self._globalCommands
    
    def isLocalCommand(self, command):
        return command.upper() in self._localCommands
    
    def processLocalMessage(self, commandKeyWord):
        if commandKeyWord == "READ":
            return ReadCommand()
        elif commandKeyWord == "OBJECTS":
            return ReadObjectsCommand()
        else:
            logging.error("Unexpected command keyword.")
    
    def translateIntoCollabAPICommand(self, message):
        tokens = self.tokenize(message)
        
        command = ''

        # Format: CREATE-VIEW [Mapname] {[Types]} [ViewName]
        # Format Lowkey: CREATE_VIEW -typedBy [type] -name [Mapname] -viewName [ViewName] -types {[Types]}
        if tokens[0].upper() == 'CREATE-VIEW':
            userCommand, mapName, types, viewName = tokens
            command += 'CREATE_VIEW -{} {} -name {} -viewName {} -types {}'.format(Literals.TYPED_BY, MindMapPackage.TYPES.MINDMAP,
                                                            mapName, viewName, types)
        elif tokens[0].upper() == 'CREATE':
            userCommand, type, name = tokens 
            command += '{} -{} {} -{} {}'.format(userCommand, Literals.TYPED_BY, type, Literals.NAME, name)
            
            if type == MindMapPackage.TYPES.MINDMAP:
                command += ' -{} {}'.format(MindMapPackage.TITLE, name)
            elif type == MindMapPackage.TYPES.MARKER:
                command += ' -{} {}'.format(MindMapPackage.MARKER_SYMBOL, name)
        elif tokens[0].upper() == 'LINK':
            userCommand, sourceAndPort, _toKeyWord, target = tokens
            source, name = sourceAndPort.split('.')
            command += '{} -from {} -to {} -{} {}'.format(userCommand, source, target, Literals.NAME, name)
        elif tokens[0].upper() == 'UPDATE':
            userCommand, clabjectName, attributeName, newValue = tokens
            command += '{} -{} {} -{} {}'.format(userCommand, Literals.NAME, clabjectName, attributeName, newValue)
        else:
            raise Error("Unexpected mindmap command.")
        
        return command
