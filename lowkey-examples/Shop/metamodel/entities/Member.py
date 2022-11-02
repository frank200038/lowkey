from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes.Entity import Entity
from metamodel import ShopPackage

class Member(Entity):
    def __init__(self, clabject:Clabject=None):
        if not clabject:
            clabject = Clabject()
            clabject.setType(ShopPackage.MEMBER)
        super().__init__(clabject)

    # Purchase
    # FROM: 1..1
    # TO: 0..*
    def getShop(self):
        shopAssociations = [a for a in self.getModel().getAssociationsByName(ShopPackage.ASSOCIATION_SHOP_MEMBER) if a.getTo() == self._clabject]

        if len(shopAssociations) > 0:
            return shopAssociations[0].getFrom()
        return None

    def removeShop(self):
        model = self.getModel()
        shopAssociations = [a for a in model.getAssociationsByName(ShopPackage.ASSOCIATION_SHOP_MEMBER) if a.getTo() == self._clabject]

        if shopAssociations:
            model.removeNode(shopAssociations[0])


    def setShop(self, shop):
        self.removeShop()

        if shop:
            shopAssociation = Association()
            shopAssociation.setName(ShopPackage.ASSOCIATION_SHOP_MEMBER)
            shopAssociation.setFrom(shop)
            shopAssociation.setTo(self)
            shopAssociation.setComposition(False)

            self.getModel().addNode(shopAssociation)


    # Product
    # FROM: 1..1
    # TO: 0..*
    def getProducts(self):
         productAssociations = [a for a in self.getModel().getAssociationsByName(ShopPackage.ASSOCIATION_PRODUCT_MEMBER) if a.getFrom() == self._clabject]

         return [a.getTo() for a in productAssociations]

    def addProduct(self, product):
         productAssociation = Association()
         productAssociation.setName(ShopPackage.ASSOCIATION_PRODUCT_MEMBER)
         productAssociation.setFrom(self)
         productAssociation.setTo(product)
         productAssociation.setComposition(False)

         self.getModel().addNode(productAssociation)

    def removeProduct(self, product):
         model = self.getModel()
         productAssociations = [a for a in model.getAssociationsByName(ShopPackage.ASSOCIATION_PRODUCT_MEMBER) if a.getFrom() == self._clabject and a.getTo() == product]

         for a in productAssociations:
             if a.getTo() == product:
                 model.removeNode(a)
                 return

    # member ID : Attribute
    # Unique, String
    def getMemberID(self):
        return self.getAttribute(ShopPackage.MEMBER_ID)

    def setMemberID(self, memberID):
        self.setAttribute(ShopPackage.MEMBER_ID, memberID)

    # member Name : Attribute
    # String
    def getMemberName(self):
        return self.getAttribute(ShopPackage.MEMBER_NAME)

    def setMemberName(self, memberName):
        self.setAttribute(ShopPackage.MEMBER_NAME, memberName)

