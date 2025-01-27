import logging
import os
import sys
import uuid

from lowkey.collabapi.commands.CreateClabjectCommand import CreateClabjectCommand
from lowkey.collabtypes import Literals

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from Command.ReadCommand import ReadCommand
from Command.ReadObjectsCommand import ReadObjectsCommand
from Command.PrintViewCommand import PrintViewCommand

from metamodel import ShopPackage


class DSLParser():
    """
    Responsible of converting Shop commands into universal commands of Lowkey
    """
    _globalCommands = ["APPLYVIEW","CREATEVIEWPOINT","UPDATEVPTYPE", "CREATE", "LINK", "UPDATE", "DELETE"]
    _localCommands = ["READ", "OBJECTS","SHOWVIEW"]

    def tokenize(self, message):
        return message.split()

    def isGlobalCommand(self, command):
        return command.upper() in self._globalCommands

    def isLocalCommand(self, command):
        return command.upper() in self._localCommands

    def processLocalMessage(self, message):
        pass
    def processLocalMessage(self, commandKeyWord):
        if commandKeyWord == "READ":
            return ReadCommand()
        elif commandKeyWord == "OBJECTS":
            return ReadObjectsCommand()
        elif commandKeyWord == "SHOWVIEW":
            viewName = input("Enter the name of the view: ")
            return PrintViewCommand(viewName)
        else:
            logging.error("Unexpected command keyword.")

    def translateIntoCollabAPICommand(self, message):
        tokens = self.tokenize(message)

        command = ''

        # Format: APPLYVIEW [EntityName] [ViewPointName] [ViewName]
        # Format Lowkey: APPLYVIEW -name [ViewName] -applyOn [EntityName] -viewPoint [ViewPointName]
        # Entity name has to be the name of the node (Never change once created)
        if tokens[0].upper() == "APPLYVIEW":
            userCommand, entityName, viewPointName, viewName = tokens
            command += "APPLYVIEW -name {} -applyOn {} -viewPoint {}".format(viewName, entityName, viewPointName)

            return command

        # Format: CREATEVIEWPOINT {[Types]} [ViewPointName]
        # Format Lowkey: CREATEVIEWPOINT -typedBy [type] -viewPointName [ViewPointName] -types {[Types]}
        elif tokens[0].upper() == 'CREATEVIEWPOINT':
            userCommand, types, viewName = tokens
            command += 'CREATEVIEWPOINT -{} {} -viewPointName {} -types {}'.format(Literals.TYPED_BY,
                                                                                   ShopPackage.TYPES.SHOP,
                                                                                  viewName, types)
            return command

        elif tokens[0].upper() == "CREATE" and len(tokens) >= 3:
            userCommand = tokens[0]
            types = tokens[1]
            name = tokens[2]
            command += '{} -{} {} -{} {}'.format(userCommand, Literals.TYPED_BY, types, Literals.NAME, name)

            # Special : Product has a price
            if types == ShopPackage.TYPES.BOOK or types == ShopPackage.TYPES.CD or types == ShopPackage.TYPES.FILM:
                if len(tokens) >= 4:
                    price = tokens[3]
                    command += ' -{} {}'.format(ShopPackage.PRODUCT_PRICE, price)
                else:
                    return None

            # ID is generated randomly using uuid
            id = str(uuid.uuid4()).replace('-', '')
            if types == ShopPackage.TYPES.SHOP:
                command += ' -{} {} -{} {}'.format(ShopPackage.SHOP_NAME, name, ShopPackage.SHOP_ID, id)
            elif types == ShopPackage.TYPES.ORDER:
                command += ' -{} {}'.format(ShopPackage.ORDER_ID, id)
            elif types == ShopPackage.TYPES.MEMBER:
                command += ' -{} {} -{} {}'.format(ShopPackage.MEMBER_NAME, name, ShopPackage.MEMBER_ID, id)
            elif types == ShopPackage.TYPES.EMPLOYEE:
                command += ' -{} {} -{} {}'.format(ShopPackage.EMPLOYEE_NAME, name, ShopPackage.EMPLOYEE_ID, id)
            elif len(tokens) == 4 and (
                    types == ShopPackage.TYPES.BOOK or types == ShopPackage.TYPES.CD or types == ShopPackage.TYPES.FILM):
                command += ' -{} {} -{} {} -{} {}'.format(ShopPackage.PRODUCT_NAME, name, ShopPackage.PRODUCT_ID, id, Literals.SUPER_TYPED_BY, ShopPackage.TYPES.PRODUCT)
            else:
                return None

            return command

        elif tokens[0].upper() == "UPDATEVPTYPE" and len(tokens) == 3:
            userCommand, viewName, types = tokens
            command += 'UPDATEVPTYPE -viewPointName {} -types {}'.format(viewName, types)
            return command

        elif tokens[0].upper() == "LINK" and len(tokens) == 4:
            userCommand, sourceAndPort, _toKeyWord, target = tokens
            source, name = sourceAndPort.split('.')
            command += '{} -from {} -to {} -{} {}'.format(userCommand, source, target, Literals.NAME, name)
            return command

        elif tokens[0].upper() == "UPDATE" and len(tokens) == 4:
            userCommand, clabjectName, attributeName, newValue = tokens
            command += '{} -{} {} -{} {}'.format(userCommand, Literals.NAME, clabjectName, attributeName, newValue)
            return command
        else:
            return None


        #TODO : Remove

