import sys
import os

from lowkey.collabapi.commands.Command import Command

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "\..")

from facilities import PrintHelper

class ReadCommand(Command):
    def execute(self, session):
        root = session.getModels()[0]
        # PrintHelper.printShop(root)
        shopClabjects = root.getShops()

        if shopClabjects:
            for shop in shopClabjects:
                PrintHelper.printShop(shop)
        else:
            print("No shops defined yet")
