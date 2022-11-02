from lowkey.collabtypes.Association import Association
from lowkey.collabtypes.Clabject import Clabject
from .Product import Product
from metamodel import ShopPackage

class Book(Product):
    def __init__(self, clabject:Clabject=None):
        if not clabject:
            clabject = Clabject()
            clabject.setType(ShopPackage.BOOK)
        super().__init__(clabject)