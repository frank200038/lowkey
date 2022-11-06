from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes.Entity import Entity
from metamodel import ShopPackage

class Order(Entity):
    def __init__(self, clabject:Clabject=None):
        if not clabject:
            clabject = Clabject()
            clabject.setType(ShopPackage.TYPES.ORDER)
        super().__init__(clabject)

    # Product
    # FROM: 1..1
    # TO: 1..*
    def getProducts(self):
        productAssociations = [a for a in self.getModel().getAssociationsByName(ShopPackage.ASSOCIATION_ORDER_PRODUCT) if a.getFrom() == self._clabject]

        return [a.getTo() for a in productAssociations]

    def removeProduct(self, product):
        model = self.getModel()
        productAssociations = [a for a in model.getAssociationsByName(ShopPackage.ASSOCIATION_ORDER_PRODUCT) if a.getFrom() == self._clabject]

        for productAssociation in productAssociations:
            if productAssociation.getTo() == product:
                model.removeNode(productAssociation)
                return

    def addProduct(self, product):
        productAssociation = Association()
        productAssociation.setName(ShopPackage.ASSOCIATION_ORDER_PRODUCT)
        productAssociation.setFrom(self)
        productAssociation.setTo(product)
        productAssociation.setComposition(True)

        self.getModel().addNode(productAssociation)

    # Member
    # FROM: 1..1
    # TO: 1..*
    def getMember(self):
        memberAssociations = [a for a in self.getModel().getAssociationsByName(ShopPackage.ASSOCIATION_MEMBER_ORDER) if a.getTo() == self._clabject]

        if len(memberAssociations) > 0:
            return memberAssociations[0].getFrom()
        return None

    # order ID : Attribute
    # Unique, String
    def getOrderID(self):
        return self.getAttribute(ShopPackage.ORDER_ID)
