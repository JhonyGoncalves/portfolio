import sqlite3
from random import randint

class Product:
    generated_ids = []  # Lista de IDs gerados

    def __init__(self, name, category, acpt_stock, price):
        self.name = name
        self.category = category
        self.acpt_stock = acpt_stock
        self.price = price
        self.id = self.create_id()

    def __str__(self):
        return f"{self.id}"

    @classmethod
    def load_ids_from_db(cls):
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM product")
        rows = cursor.fetchall()
        cls.generated_ids = [row[0] for row in rows]
        connection.close()

    def create_id(self):
        while True:
            id_str = ''.join([str(randint(0, 9)) for _ in range(10)])
            if id_str not in Product.generated_ids:
                Product.generated_ids.append(id_str)
                return int(id_str)  
