from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes.Entity import Entity
from metamodel import ShopPackage

class Product(Entity):

    def __init__(self, clabject: Clabject = None):
        assert clabject
        super().__init__(clabject)

    def update(self):
        self.getPersistence()

    # product ID : Attribute
    # Unique, String
    def getProductID(self):
        return self.getAttribute(ShopPackage.PRODUCT_ID)

    def setProductID(self, productID):
        self.setAttribute(ShopPackage.PRODUCT_ID, productID)

    # Product Name: Attribute
    # String
    def getProductName(self):
        return self.getAttribute(ShopPackage.PRODUCT_NAME)

    def setProductName(self, productName):
        self.setAttribute(ShopPackage.PRODUCT_NAME, productName)

    # Price: Attribute
    # Int
    def getPrice(self):
        return self.getAttribute(ShopPackage.PRODUCT_PRICE)

    def setPrice(self, price):
        self.setAttribute(ShopPackage.PRODUCT_PRICE, price)

