class TYPES():
    SHOP = "Shop"
    MEMBER = "Member"
    EMPLOYEE = "Employee"
    BOOK = "Book"
    CD = "CD"
    FILM = "Film"
    ORDER = "Order"
    PRODUCT = "Product"
    TYPES = [SHOP, MEMBER, EMPLOYEE, BOOK, CD, FILM, ORDER, PRODUCT]

TITLE = "title"

ASSOCIATION_SHOP_MEMBER = "members"
ASSOCIATION_MEMBER_ORDER = "orders"
ASSOCIATION_ORDER_PRODUCT= "products"
ASSOCIATION_SHOP_EMPLOYEE = "employees"

MEMBER_ID = "memberID"
MEMBER_NAME = "memberName"

ORDER_ID = "orderID"

PRODUCT_ID = "productID"
PRODUCT_NAME = "productName"
PRODUCT_PRICE = "price"

EMPLOYEE_ID = "employeeID"
EMPLOYEE_NAME = "employeeName"

SHOP_ID = "shopID"
SHOP_NAME = "shopName"