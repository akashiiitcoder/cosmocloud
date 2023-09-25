from datetime import datetime
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from pymongo import MongoClient, ReturnDocument
from db import db
from models import Product, Order
from seed_data import seed_dummy_products

app = FastAPI()

# Seed dummy products into the database
seed_dummy_products()

# Declare a global variable to cache all the products
#since there are only few products we can cache all of them
productsCache = {}

# Endpoint to list all available products
@app.get("/products")
def list_products():
    try:
        # Check if products are already cached
        products = list(productsCache.values())
        if not products: 
            # Fetch products from database
            productCursor = db.products.find()
            # Raise exception if no products are found
            if(productCursor.count() == 0):
                raise HTTPException(status_code=404, detail="No products found")
            # Convert products to list of Product objects
            products = [Product(**product) for product in productCursor]
            # Create a dictionary that maps product IDs to products
            productsCache = {str(product["_id"]): product for product in products}
        # Create success message with number of products found
        message = {"message": "Success! Found {} products".format(len(products))}
        # Create response content with message and products list
        responseContent = {"message": message, "products": products}
        # Return response with 200 status code
        return JSONResponse(content=responseContent, status_code=200)
    except Exception as e:
        # Return error message if there was an error while fetching products
        return {"message": "Error while fetching products: {}".format(str(e))}

# Endpoint to create a new order
@app.post("/orders")
def create_order(order: Order):
    try:
        # Start a transaction to create the order
        with db.client.start_session() as session:
            with session.start_transaction():
                # Check if products are already cached
                if not productsCache:
                    # Fetch products from database
                    productCursor = db.products.find()
                    # Raise exception if no products are found
                    if(productCursor.count() == 0):
                        raise HTTPException(status_code=404, detail="No products found")
                    # Convert products to list of Product objects
                    products = [Product(**product) for product in productCursor]
                    # Create a dictionary that maps product IDs to products
                    productsCache = {str(product["_id"]): product for product in products}

                # Check if all the products are available in the required quantity
                for item in order.items:
                    # Fetch product from cache
                    product = productsCache.get(str(item.product_id))
                    # If product is not available, raise an exception
                    if product.available_quantity < item.bought_quantity:
                        raise HTTPException(status_code=400, detail="Product not available")

                total_amount = 0
                order_id = None

                for item in order.items:
                    # Fetch product from cache
                    product = productsCache.get(str(item.product_id))
                    # Update product available quantity
                    product.available_quantity -= item.bought_quantity
                    # Update product in the database
                    response=update_product_quantity(product["_id"], product.available_quantity)
                    if response is None:
                        raise HTTPException(status_code=404, detail="Product not found in database, Inconsistent Cache")
                    # Calculate total amount of the order
                    total_amount = total_amount + (product.price * item.bought_quantity)
                
                # Insert order into the database
                order = Order(
                    timestamp=datetime.now(),
                    items=order.items,
                    total_amount=total_amount,
                    user_address=order.user_address
                )
                order_id = db.orders.insert_one(document=order).inserted_id
                # If order was not created, raise an exception
                if not order_id:
                    raise HTTPException(status_code=400, detail="Order not created")
                # Create success message with order ID
                message = {"message": "Success! Created order with ID: {}".format(order_id)}
                # Create response content with message and order ID
                responseContent = {"message": message, "order_id": order_id}
                # Return response with 200 status code
                return JSONResponse(content=responseContent, status_code=200)
    except Exception as e:
        # Return error message if there was an error while fetching orders
        return {"message": "Error while creating order: {}".format(str(e))}

# Endpoint to list all orders with pagination
@app.get("/orders")
def get_orders(limit: int = Query(default=10, description="Number of records per page", le=50), 
               offset: int = Query(default=0, description="Page offset", ge=0)):
    try:
        # Count total number of orders
        totalOrders = db.orders.count_documents({})
        # Raise exception if no orders are found
        if totalOrders == 0:
            raise HTTPException(status_code=404, detail="No orders found")
        # Fetch orders with pagination and sorting to fetch most recent orders first
        ordersCursor = db.orders.find().sort("_id", -1).skip(offset).limit(limit)
        # Convert orders to list of Order objects
        orders = [Order(**order) for order in ordersCursor]
        # Create success message with number of orders found
        message = {"message": "Success! Found {} orders".format(len(orders))}
        # Create response content with message, orders list, and pagination metadata
        responseContent = {
            "message": message,
            "orders": orders,
            "pagination": {
                "total": totalOrders,
                "limit": limit,
                "offset": offset,
                "has_next": offset + limit < totalOrders,
                "has_previous": offset > 0
            }
        }
        # Return response with 200 status code
        return JSONResponse(content=responseContent, status_code=200)
    except Exception as e:
        # Return error message if there was an error while fetching orders
        return {"message": "Error while fetching orders: {}".format(str(e))}

# Endpoint to fetch a single order by Order ID
@app.get("/orders/{order_id}")
def fetch_order(order_id: str):
    try:
        # Find order in database by ID
        order = db.orders.find_one({"_id": ObjectId(order_id)})
        # Raise exception if order is not found
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        # Convert order to Order object by unpacking
        order = Order(**order)
        # Create success message with order ID
        message = {"message": "Success! Found order with ID: {}".format(order_id)}
        # Create response content with message and order
        responseContent = {"message": message, "order": order}
        # Return response with 200 status code
        return JSONResponse(content=responseContent, status_code=200)
    except Exception as e:
        # Return error message if there was an error while fetching order
        return {"message": "Error while fetching order: {}".format(str(e))}

# Endpoint to update product available quantity
@app.put("/products/{product_id}")
def update_product_quantity(product_id: ObjectId, quantity: int):
    try:
        # Update the product in the database
        updatedProduct = db.products.find_one_and_update(
            {"_id": product_id},
            {"$set": {"available_quantity": quantity}},
            return_document=ReturnDocument.AFTER
        )
        # If the product was not found, return a 404 error
        if updatedProduct is None:
            raise HTTPException(status_code=404, detail="Product not found in database, Inconsistent Cache")
        # Update the product in the productsCache dictionary
        productsCache[str(product_id)] = Product(**updatedProduct)
        # Return the updated product
        return updatedProduct
    except Exception as e:
        # Return error message if there was an error while updating product
        return {"message": "Error while updating product: {}".format(str(e))}
