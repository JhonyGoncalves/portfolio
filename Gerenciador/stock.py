from product import Product

class Stock:
    def __init__(self, product : Product, quantity, location):
        self.product = product
        self.quantity = quantity
        self.location = location
    def __str__(self):
        return (f"Produto:{self.product}, Quantidade:{self.quantity}, Localização:{self.location}")