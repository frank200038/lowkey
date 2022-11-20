import logging
import os
import sys

from lowkey.collabapi.commands.Command import Command


from lowkey.lww.LWWVertex import LWWVertex
from metamodel import ShopPackage
from metamodel.entities.Member import Member
from metamodel.entities.Product import Product
from metamodel.entities.Employee import Employee
from metamodel.entities.Order import Order

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


class PrintViewCommand(Command):

    def __init__(self, viewName):
        self._viewName = viewName

    def execute(self, session):
        # logging.debug(" Executing command 'SHOWVIEW' in session {}.".format(session._id))
        root = session.getModels()[0]

        view = root.getViewByName(self._viewName)

        if view is None:
            print("View not found")
            return
        else:
            printer = ViewPrintHelper(view)
            printer.printView()

class ViewPrintHelper():

    def __init__(self, view):
        self._view = view

    def printView(self):
        self._view.update()
        self.__printView(self._view.getRoots())

    def __printView(self, vertices: [LWWVertex], depth=0):
        """
        Prints the view in a tree-like structure (Recursively)

        :param vertices: vertices contained at the current depth in the tree
        :param depth: Depth of the tree, used to indent the print
        """
        for vertex in vertices:
            space = ' ' * depth
            node = vertex.query("nodes")
            name = self.__findNameOfNode(node)
            print(space + name)
            adjacentVertices = self._view.getAdjacencyListForVertex(vertex)
            self.__printView(adjacentVertices, depth + 1)

    def __findNameOfNode(self, node):

        type = node.getType()
        if type == ShopPackage.TYPES.MEMBER:
            member = Member(clabject = node)
            return member.getMemberName()
        elif type == ShopPackage.TYPES.EMPLOYEE:
            employee = Employee(clabject = node)
            return employee.getEmployeeName()
        elif type == ShopPackage.TYPES.ORDER:
            order = Order(clabject = node)
            return order.getOrderID()
        elif type == ShopPackage.TYPES.FILM or type == ShopPackage.TYPES.CD or type == ShopPackage.TYPES.BOOK:
            product = Product(clabject = node)
            return product.getProductName()
