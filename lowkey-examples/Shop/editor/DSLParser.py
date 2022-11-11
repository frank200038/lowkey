import logging
import os
import sys
import uuid

from lowkey.collabapi.commands.CreateClabjectCommand import CreateClabjectCommand
from lowkey.collabtypes import Literals

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from Command.ReadCommand import ReadCommand
from Command.ReadObjectsCommand import ReadObjectsCommand

from metamodel import ShopPackage


class DSLParser():
    _globalCommands = ["APPLYVIEW","CREATEVIEWPOINT", "CREATE", "LINK", "UPDATE", "DELETE"]
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
        if tokens[0].upper() == "APPLYVIEW":
            userCommand, entityName, viewPointName, viewName = tokens
            command += "APPLYVIEW -name {} -applyOn {} -viewPoint {}".format(viewName, entityName, viewPointName)

            return command
        # Format: CREATEVIEW [ShopName] {[Types]} [ViewName]
        # Format Lowkey: CREATEVIEW -typedBy [type] -name [ShopName] -viewName [ViewName] -types {[Types]}
        elif tokens[0].upper() == 'CREATEVIEW':
            userCommand, mapName, types, viewName = tokens
            command += 'CREATEVIEW -{} {} -name {} -viewName {} -types {}'.format(Literals.TYPED_BY,
                                                                                   ShopPackage.TYPES.SHOP,
                                                                                   mapName, viewName, types)
            return command

        if tokens[0].upper() == "CREATE" and len(tokens) >= 3:
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
            if types == ShopPackage.TYPES.SHOP and len(tokens) == 3:
                command += ' -{} {} -{} {} -for NONE'.format(ShopPackage.SHOP_NAME, name, ShopPackage.SHOP_ID, id)
            elif types == ShopPackage.TYPES.ORDER and len(tokens) == 4:
                command += ' -{} {} -for {}'.format(ShopPackage.ORDER_ID, id, tokens[-1])
            elif types == ShopPackage.TYPES.MEMBER and len(tokens) == 4:
                command += ' -{} {} -{} {} -for {}'.format(ShopPackage.MEMBER_NAME, name, ShopPackage.MEMBER_ID, id, tokens[-1])
            elif types == ShopPackage.TYPES.EMPLOYEE and len(tokens) == 4:
                command += ' -{} {} -{} {} -for {}'.format(ShopPackage.EMPLOYEE_NAME, name, ShopPackage.EMPLOYEE_ID, id, tokens[-1])
            elif len(tokens) == 5 and (
                    types == ShopPackage.TYPES.BOOK or types == ShopPackage.TYPES.CD or types == ShopPackage.TYPES.FILM):
                command += ' -{} {} -{} {} -for {}'.format(ShopPackage.PRODUCT_NAME, name, ShopPackage.PRODUCT_ID, id, tokens[-1])
            else:
                return None

            return command

        elif tokens[0].upper() == "LINK" and len(tokens) == 5:
            userCommand, sourceAndPort, _toKeyWord, target, forEntity = tokens
            source, name = sourceAndPort.split('.')
            command += '{} -from {} -to {} -{} {} -for {}'.format(userCommand, source, target, Literals.NAME, name,
                                                                  forEntity)
            return command
        else:
            return None

        # TODO : Update & Remove


# test = DSLParser()
# print(test.translateIntoCollabAPICommand("CREATE Shop Shop1"))
# print(test.translateIntoCollabAPICommand("CREATE Member Member1 Shop1"))
# print(test.translateIntoCollabAPICommand("CREATE Employee Employee1 Shop1"))
# print(test.translateIntoCollabAPICommand("CREATE Order Order1 Shop1"))
# print(test.translateIntoCollabAPICommand("CREATE Book Book1 10 Shop1"))
# print(test.translateIntoCollabAPICommand("CREATE CD CD1 10 Shop1"))
# print(test.translateIntoCollabAPICommand("CREATE Film Film1 10 Shop1"))
# print(test.translateIntoCollabAPICommand("LINK Shop1.employees TO Employee1 Shop1"))
# print(test.translateIntoCollabAPICommand("LINK Shop1.members TO Member1 Shop1"))
# print(test.translateIntoCollabAPICommand("LINK Member1.orders TO Order1 Shop1"))
# print(test.translateIntoCollabAPICommand("LINK Order1.products TO Book1 Shop1"))
# print(test.translateIntoCollabAPICommand("LINK Order1.products TO CD1 Shop1"))
# print(test.translateIntoCollabAPICommand("LINK Order1.products TO Film1 Shop1"))


