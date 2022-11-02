from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from lowkey.collabtypes.Entity import Entity
from metamodel import ShopPackage

class Shop(Entity):
    def __init__(self, clabject:Clabject=None):
        if not clabject:
            clabject = Clabject()
            clabject.setType(ShopPackage.SHOP)
        super().__init__(clabject)

    # Employee
    # FROM: 1..1
    # TO: 0..*
    def getEmployees(self):
        employeeAssociations = [a for a in self.getModel().getAssociationsByName(ShopPackage.ASSOCIATION_SHOP_EMPLOYEE) if a.getFrom() == self._clabject]

        employees = []
        for a in employeeAssociations:
            employees.append(a.getTo())
        return employees

    def addEmployee(self, employee):
        employeeAssociation = Association()
        employeeAssociation.setName(ShopPackage.ASSOCIATION_SHOP_EMPLOYEE)
        employeeAssociation.setFrom(self)
        employeeAssociation.setTo(employee)
        employeeAssociation.setComposition(False)

        self.getModel().addNode(employeeAssociation)

    def removeEmployee(self, employee):
        model = self.getModel()
        employeeAssociations = [a for a in model.getAssociationsByName(ShopPackage.ASSOCIATION_SHOP_EMPLOYEE) if a.getFrom() == self._clabject]

        for a in employeeAssociations:
            if a.getTo() == employee:
                model.removeNode(a)
                return

    # Member
    # FROM: 1..1
    # TO: 0..*
    def getMembers(self):
        memberAssociations = [a for a in self.getModel().getAssociationsByName(ShopPackage.ASSOCIATION_SHOP_MEMBER) if a.getFrom() == self._clabject]

        members = []
        for a in memberAssociations:
            members.append(a.getTo())
        return members

    def addMember(self, member):
        memberAssociation = Association()
        memberAssociation.setName(ShopPackage.ASSOCIATION_SHOP_MEMBER)
        memberAssociation.setFrom(self)
        memberAssociation.setTo(member)
        memberAssociation.setComposition(False)

        self.getModel().addNode(memberAssociation)

    def removeMember(self, member):
        model = self.getModel()
        memberAssociations = [a for a in model.getAssociationsByName(ShopPackage.ASSOCIATION_SHOP_MEMBER) if a.getFrom() == self._clabject]

        for a in memberAssociations:
            if a.getTo() == member:
                model.removeNode(a)
                return

    # shopID : Attribute
    # unique, String
    def getShopID(self):
        return self.getAttribute(ShopPackage.SHOP_ID)

    def setShopID(self, shopID):
        self.setAttribute(ShopPackage.SHOP_ID, shopID)
