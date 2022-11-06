from lowkey.collabtypes.Model import Model
from metamodel.entities.Shop import Shop
from metamodel.entities.Order import Order
from metamodel.entities.Product import Product
from metamodel.entities.Member import Member
from metamodel.entities.Employee import Employee
from metamodel.entities.Film import Film
from metamodel.entities.CD import CD
from metamodel.entities.Book import Book

def printShop(shopClabject):
    shop = Shop(clabject = shopClabject)

    print("\nPrinting Shop of name {} with ID {}".format(shop.getShopName(), shop.getShopID()))
    print("====================================================================================")

    print("This shop has the following members with details: ")
    members = shop.getMembers()
    if len(members) > 0:
        for member in members:
            printMember(member)
    else:
        print("No Members found")

    print()

    print("This shop has the following employees:")
    employees = shop.getEmployees()
    if len(employees) > 0:
        for employee in employees:
            printEmployee(employee)
    else:
        print("No Employees found")

def printMember(memberClabject):
    member = Member(clabject = memberClabject)

    print(" Member of name {} with ID {} has the following orders:".format(member.getMemberName(), member.getMemberID()))


    orders = member.getOrders()
    if len(orders) > 0:
        for order in orders:
            printOrder(order)
    else:
        print("  No Orders found")

def printOrder(orderClabject):
    order = Order(clabject = orderClabject)

    print("     -- Order with ID {} with following products".format(order.getOrderID()))

    products = order.getProducts()
    if len(products) > 0:
        for product in products:
            printProduct(product)
    else:
        print("      No Products found")

def printProduct(productClabject):
    product = Product(clabject = productClabject)

    print("         -- Product of name {} with ID {} and price {} and type {}".format(product.getProductName(), product.getProductID(), product.getPrice(), productClabject.getType()))

def printEmployee(employeeClabject):
    employee = Employee(clabject = employeeClabject)

    print(" Employee of name {} with ID {}".format(employee.getEmployeeName(), employee.getEmployeeID()))
