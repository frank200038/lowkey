from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes.Entity import Entity
from metamodel import ShopPackage

class Employee(Entity):
    def __init__(self, clabject:Clabject = None):
        if not clabject:
            clabject = Clabject()
            clabject.setType(ShopPackage.Employee)
        super().__init__(clabject)

    # Shop
    # FROM: 0..*
    # TO: 1..1
    def getShop(self):
        shopAssociations = [a for a in self.getModel().getAssociationsByName(ShopPackage.ASSOCIATION_SHOP_EMPLOYEE) if a.getTo() == self._clabject]
        if len(shopAssociations) == 0:
            return None
        return shopAssociations[0].getFrom()

    def removeShop(self):
        model = self.getModel()
        shopAssociations = [a for a in model.getAssociationsByName(ShopPackage.ASSOCIATION_SHOP_EMPLOYEE) if a.getTo() == self._clabject]

        if shopAssociations:
            model.removeNode(shopAssociations[0])\

    def setShop(self, shop):
        self.removeShop()

        if shop:
            shopAssociation = Association()
            shopAssociation.setName(ShopPackage.ASSOCIATION_SHOP_EMPLOYEE)
            shopAssociation.setFrom(shop)
            shopAssociation.setTo(self)
            shopAssociation.setComposition(False)

            self.getModel().addNode(shopAssociation)

    # Employee ID : Attribute
    # Unique, String
    def getEmployeeID(self):
        return self.getAttribute(ShopPackage.EMPLOYEE_ID)

    def setEmployeeID(self, employeeID):
        self.setAttribute(ShopPackage.EMPLOYEE_ID, employeeID)

    # Employee Name : Attribute
    # String
    def getEmployeeName(self):
        return self.getAttribute(ShopPackage.EMPLOYEE_NAME)

    def setEmployeeName(self, employeeName):
        self.setAttribute(ShopPackage.EMPLOYEE_NAME, employeeName)
