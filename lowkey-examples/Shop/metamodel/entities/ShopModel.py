from lowkey.collabtypes.Model import Model
from metamodel import ShopPackage

from .Shop import Shop

class ShopModel(Model):

    def __init__(self, title=""):
        super().__init__()
        self.setTitle(title)

    def getTitle(self):
        return self.getAttribute(ShopPackage.TITLE)

    def setTitle(self, title):
        self.setAttribute(ShopPackage.TITLE, title)

    def getShops(self):
        return [c for c in self.getClabjects() if c.getType() == ShopPackage.TYPES.SHOP]

    def getShopsByName(self, name):
        return [c for c in self.getClabjects() if c.getType() == ShopPackage.TYPES.SHOP and c.getName(name)]