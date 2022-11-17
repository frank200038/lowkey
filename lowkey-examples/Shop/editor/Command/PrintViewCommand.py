import logging
import os
import sys

from lowkey.collabapi.commands.Command import Command


from lowkey.lww.LWWVertex import LWWVertex

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


class PrintViewCommand(Command):

    def __init__(self, viewName):
        self._viewName = viewName

    def execute(self, session):
        logging.debug(" Executing command 'SHOWVIEW' in session {}.".format(session._id))
        root = session.getModels()[0]
        view = root.getViewByName(self._viewName)
        printer = ViewPrintHelper(view)
        printer.printView()

class ViewPrintHelper():

    def __init__(self, view):
        self._view = view

    def printView(self):
        self.__printView(self._view.getRoots())

    def __printView(self, vertices: [LWWVertex], depth=0):
        for vertex in vertices:
            space = ' ' * depth
            print(space + vertex.query("nodes").getName())
            adjacentVertices = self._view.getAdjacencyListForVertex(vertex)
            self.__printView(adjacentVertices, depth + 1)
