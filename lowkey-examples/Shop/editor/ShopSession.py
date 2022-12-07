import os
import sys
import uuid

from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabapi.Session import Session

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from metamodel import ShopPackage
from metamodel.entities.ShopModel import ShopModel


class ShopSession(Session):
    """
    Initiate the ShopModel with the default values.
    """
    def __init__(self):
        super().__init__()
        self._shopmodel = ShopModel()
        self.addModel(self._shopmodel)

    def getShopModel(self):
        return self._shopmodel
