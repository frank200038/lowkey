from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes.Entity import Entity
from metamodel import ShopPackage

class Member(Entity):
    def __init__(self, clabject:Clabject=None):
        if not clabject:
            clabject = Clabject()
            clabject.setType(ShopPackage.TYPES.MEMBER)
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


    # Order
    # FROM: 1..1
    # TO: 0..*
    def getOrders(self):
        orderAssociations = [a for a in self.getModel().getAssociationsByName(ShopPackage.ASSOCIATION_MEMBER_ORDER) if a.getFrom() == self._clabject]

        return [a.getTo() for a in orderAssociations]

    def removeOrder(self, order):
        model = self.getModel()
        orderAssociations = [a for a in model.getAssociationsByName(ShopPackage.ASSOCIATION_MEMBER_ORDER) if a.getFrom() == self._clabject]

        for orderAssociation in orderAssociations:
            if orderAssociation.getTo() == order:
                model.removeNode(orderAssociation)
                return

    def addOrder(self, order):
        orderAssociation = Association()
        orderAssociation.setName(ShopPackage.ASSOCIATION_MEMBER_ORDER)
        orderAssociation.setFrom(self)
        orderAssociation.setTo(order)
        orderAssociation.setComposition(False)

        self.getModel().addNode(orderAssociation)

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

