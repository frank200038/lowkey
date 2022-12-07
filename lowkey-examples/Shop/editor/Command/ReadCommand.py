import sys
import os

from lowkey.collabapi.commands.Command import Command

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from facilities import PrintHelper

class ReadCommand(Command):
    """
    Print a Shop instance in a tree structure with all the details in a readable format.
    """
    def execute(self, session):
        root = session.getModels()[0]
        # PrintHelper.printShop(root)
        shopClabjects = root.getShops()

        if shopClabjects:
            for shop in shopClabjects:
                PrintHelper.printShop(shop)
        else:
            print("No shops defined yet")
