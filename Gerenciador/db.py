import sqlite3

def create_tables():
    connector = sqlite3.connect('products.db')
    cursor = connector.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            ID INTEGER PRIMARY KEY, 
            name TEXT, 
            category TEXT, 
            acpt_stock INTEGER, 
            price REAL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            ID INTEGER PRIMARY KEY, 
            quantity INTEGER, 
            location TEXT
        )
    """)
    
    connector.commit()
    connector.close()

# Chame esta função antes de iniciar o aplicativo principal
create_tables()
