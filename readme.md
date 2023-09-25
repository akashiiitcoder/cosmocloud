E-commerce API
This is an API for an e-commerce website that allows users to create orders for products. The API is built using Python and the FastAPI framework, and it uses MongoDB as the database.

Installation
To install the dependencies for this project, run the following command:

Usage
To start the API server, run the following command:

This will start the server on http://localhost:8000.

Endpoints
The following endpoints are available:

**GET /products**
The list_products endpoint is a GET endpoint that returns a list of all available products in the e-commerce application. The endpoint is defined using the @app.get decorator from the FastAPI framework, which maps the endpoint to the /products URL.

The function first checks if the products are already cached in memory. If the products are cached, the function retrieves the products from the cache. If the products are not cached, the function retrieves the products from the database using the find() method of the db.products collection.

If no products are found in the database, the function raises an HTTPException with a status code of 404 and a detail message of "No products found". This ensures that clients receive a clear and informative error message if there are no products available.

The function then converts the products to a list of Product objects using a list comprehension. The Product class is defined in the models module and represents a single product in the e-commerce application. The Product class is defined using the pydantic.BaseModel class, which provides a simple and efficient way to define data models in Python.

The function then creates a dictionary that maps product IDs to products. This dictionary is used to cache the products in memory for faster retrieval in future requests.

The function then creates a success message with the number of products found, and creates a response content dictionary with the message and the list of products. The response is returned as a JSON response using the JSONResponse class from the FastAPI framework.

If there was an error while fetching the products, the function returns an error message with the details of the error. This ensures that clients receive informative error messages if there are any issues with the API.

**POST /orders**
The create_order endpoint is a POST endpoint that allows users to create a new order in the e-commerce application. The endpoint is defined using the @app.post decorator from the FastAPI framework, which maps the endpoint to the /orders URL.

The function takes an OrderCreate object as input, which is defined in the models module and represents the data required to create a new order. The OrderCreate object includes fields such as the user ID, product ID, and quantity.

The function first checks if the specified product exists in the database using the find_one() method of the db.products collection. If the product does not exist, the function raises an HTTPException with a status code of 404 and a detail message of "Product not found". This ensures that clients receive a clear and informative error message if they try to create an order for a non-existent product.

The function then checks if the specified quantity is greater than the available quantity of the product. If the quantity is greater than the available quantity, the function raises an HTTPException with a status code of 400 and a detail message of "Not enough stock available". This ensures that clients receive a clear and informative error message if they try to order more products than are available.

If the product and quantity are valid, the function creates a new order in the database using the insert_one() method of the db.orders collection. The insert_one() method returns the ID of the newly created order, which is included in the response message.

The function then updates the available quantity of the product in the database using the update_one() method of the db.products collection. The update_one() method decrements the available quantity of the product by the specified quantity.

The function then creates a success message with the ID of the newly created order, and creates a response content dictionary with the message and the ID of the order. The response is returned as a JSON response using the JSONResponse class from the FastAPI framework.

If there was an error while creating the order or updating the product quantity, the function returns an error message with the details of the error. This ensures that clients receive informative error messages if there are any issues with the API.

**GET /orders**
The get_orders endpoint is a GET endpoint that returns a list of all orders in the e-commerce application. The endpoint is defined using the @app.get decorator from the FastAPI framework, which maps the endpoint to the /orders URL.

The function takes two optional query parameters: skip and limit. These parameters are used to implement pagination, allowing clients to retrieve a subset of the orders at a time. The skip parameter specifies the number of orders to skip, and the limit parameter specifies the maximum number of orders to return.

The function retrieves the orders from the database using the find() method of the db.orders collection. The find() method returns a cursor object, which is used to iterate over the orders in the database.

The function then converts the orders to a list of Order objects using a list comprehension. The Order class is defined in the models module and represents a single order in the e-commerce application. The Order class is defined using the pydantic.BaseModel class, which provides a simple and efficient way to define data models in Python.

The function then creates a success message with the number of orders found, and creates a response content dictionary with the message and the list of orders. The response is returned as a JSON response using the JSONResponse class from the FastAPI framework.

If there was an error while fetching the orders, the function returns an error message with the details of the error. This ensures that clients receive informative error messages if there are any issues with the API.

By providing pagination support and converting the orders to a list of Order objects, this function enables clients to easily retrieve and process orders in the e-commerce application. The use of the FastAPI framework and the JSONResponse class also helps to ensure that the API is fast, reliable, and easy to use.

**GET /orders/{order_id}**
The fetch_order endpoint is a GET endpoint that retrieves a single order by ID. The endpoint is defined using the @app.get decorator from the FastAPI framework, which maps the endpoint to the /orders/{order_id} URL.

The function takes an order_id parameter as input, which is the ID of the order to retrieve. The order_id parameter is specified in the URL path using the {order_id} syntax.

The function retrieves the order from the database using the find_one() method of the db.orders collection. The find_one() method returns a single document that matches the specified query, or None if no documents match the query.

If the order is not found, the function raises an HTTPException with a status code of 404 and a detail message of "Order not found". This ensures that clients receive a clear and informative error message if they try to retrieve a non-existent order.

If the order is found, the function converts the order to an Order object using the Order.from_dict() method. The Order class is defined in the models module and represents a single order in the e-commerce application. The Order class is defined using the pydantic.BaseModel class, which provides a simple and efficient way to define data models in Python.

The function then creates a success message with the ID of the retrieved order, and creates a response content dictionary with the message and the retrieved order. The response is returned as a JSON response using the JSONResponse class from the FastAPI framework.

If there was an error while fetching the order, the function returns an error message with the details of the error. This ensures that clients receive informative error messages if there are any issues with the API.

By providing a way to retrieve a single order by ID, this function enables clients to easily retrieve and process orders in the e-commerce application. The use of the FastAPI framework and the JSONResponse class also helps to ensure that the API is fast, reliable, and easy to use.

**PUT /products/{product_id}**
The update_product_quantity endpoint is a PUT endpoint that allows users to update the quantity of a product in the e-commerce application. The endpoint is defined using the @app.put decorator from the FastAPI framework, which maps the endpoint to the /products/{product_id}/quantity URL.

The function takes two parameters as input: product_id and quantity. The product_id parameter is the ID of the product to update, and the quantity parameter is the new quantity of the product.

The function first checks if the specified product exists in the database using the find_one() method of the db.products collection. If the product does not exist, the function raises an HTTPException with a status code of 404 and a detail message of "Product not found". This ensures that clients receive a clear and informative error message if they try to update the quantity of a non-existent product.

If the product exists, the function updates the quantity of the product in the database using the update_one() method of the db.products collection. The update_one() method updates the quantity of the product with the specified ID to the new quantity.

The function then creates a success message with the ID of the updated product, and creates a response content dictionary with the message and the ID of the updated product. The response is returned as a JSON response using the JSONResponse class from the FastAPI framework.

If there was an error while updating the product quantity, the function returns an error message with the details of the error. This ensures that clients receive informative error messages if there are any issues with the API.

By providing a way to update the quantity of a product, this function enables clients to easily manage the inventory of the e-commerce application. The use of the FastAPI framework and the JSONResponse class also helps to ensure that the API is fast, reliable, and easy to use.

Documentation


Please go through the comments in the code. Due to time constraints, it was not possible to add a separate documentation.

Key optimizations:
1. indexing on _id of product and _id of orders happens automatically which leads to fast retrieval.

2. caching of products is done because there are only a few products, and it leads to fast retrieval.

3. Generating timestamp at backend to avoid conflicts/incorrect timestamps from client


Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

I hope this helps! Let me know if you have any further questions or if there's anything else I can do for you.
