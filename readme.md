E-commerce API
This is an API for an e-commerce website that allows users to create orders for products. The API is built using Python and the FastAPI framework, and it uses MongoDB as the database.

Installation
To install the dependencies for this project, run the following command:

Usage
To start the API server, run the following command:

This will start the server on http://localhost:8000.

Endpoints
The following endpoints are available:

GET /products
This endpoint returns a list of all available products.

POST /orders
This endpoint allows users to create a new order.

GET /orders
This endpoint returns a list of all orders, with pagination support.

GET /orders/{order_id}
This endpoint returns a single order by ID.

PUT /products/{product_id}
This endpoint allows users to update the available quantity of a product.

Documentation

Please go through the comments in the code. Due to time constraints, it was not possible to add a separate documentation.

Key optimizations:
1. indexing on _id of product and _id of orders happen automatically which leads to fast retrieval.

2. caching of procuts is done because there are only a few products

3. Generating timestamp at backend to avoid conflincts/incorrect timestamps from client


Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

I hope this helps! Let me know if you have any further questions or if there's anything else I can do for you.
