from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    serialnumber : str
    price: float

class ProductCreate(ProductBase):
    name: str
    description: Optional[str] = None
    serialnumber : str
    price: float

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int


    class Config:
        from_attributes = True 
