from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from metamodel import MindMapPackage

class Product(Entity):

    def __init__(self, clabject: Clabject = None):
        assert clabject
        super().__init__(clabject)

    def update(self):
        self.getPersistence()

    # Purchase
    # FROM: 1..1
    # TO: 0..*

    def getMember(self):
        memberAssociations = [a for a in self.getModel().getAssociationsByName(ShopPackage.ASSOCIATION_PRODUCT_MEMBER) if a.getTo() == self._clabject]

        if len(memberAssociations) > 0:
            return memberAssociations[0].getFrom()
        return None

    def removeMember(self):
        model = self.getModel()
        memberAssociations = [a for a in model.getAssociationsByName(ShopPackage.ASSOCIATION_PRODUCT_MEMBER) if a.getTo() == self._clabject]

        if memberAssociations:
            model.removeNode(memberAssociations[0])

    def setMember(self, member):
        self.removeMember()

        if member:
            memberAssociation = Association()
            memberAssociation.setName(ShopPackage.ASSOCIATION_PRODUCT_MEMBER)
            memberAssociation.setFrom(member)
            memberAssociation.setTo(self)
            memberAssociation.setComposition(False)

            self.getModel().addNode(memberAssociation)

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
        return self.getAttribute(ShopPackage.PRICE)

    def setPrice(self, price):
        self.setAttribute(ShopPackage.PRODUCT_PRICE, price)

