from db import db

dummy_products = [
    {"name": "Product 1", "price": 19.99, "quantity": 50},
    {"name": "Product 2", "price": 29.99, "quantity": 30},
    {"name": "Product 3", "price": 9.99, "quantity": 100},
    {"name": "Product 4", "price": 39.99, "quantity": 20},
    {"name": "Product 5", "price": 49.99, "quantity": 60},
    {"name": "Product 6", "price": 15.99, "quantity": 75},
    {"name": "Product 7", "price": 24.99, "quantity": 45},
    {"name": "Product 8", "price": 12.99, "quantity": 90},
    {"name": "Product 9", "price": 34.99, "quantity": 55},
    {"name": "Product 10", "price": 8.99, "quantity": 70},
]

def seed_dummy_products():
    # Insert dummy products into the products collection
    products_collection = db.products
    products_collection.insert_many(dummy_products)

    print("Dummy products added successfully.")
