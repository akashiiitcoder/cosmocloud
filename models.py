from pydantic import BaseModel
from typing import Optional
from typing import List
from datetime import datetime
from bson import ObjectId

class Product(BaseModel):
    name: str                           # name of the product
    price: float                        # price of the product
    available_quantity: int             # available quantity of the product

class UserAddress(BaseModel):
    city: str                           # city of the user's address
    country: str                        # country of the user's address
    zip_code: str                       # zip code of the user's address

class OrderItem(BaseModel):
    product_id: ObjectId                # reference to the product
    bought_quantity: int                # quantity bought of the product
    class Config:
        arbitrary_types_allowed = True

class Order(BaseModel):
    timestamp: Optional[datetime]       # timestamp would be generated at the backend
    items: List[OrderItem]              # list of items, a reference to the OrderItem
    total_amount: Optional[float] = 0   # total amount of the order would be calculated at the backend
    user_address: UserAddress           # user's address for the order