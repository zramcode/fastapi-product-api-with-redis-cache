from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db.database import get_db
from app.operations import crud
from app.schema import ProductCreate, Product, ProductUpdate
from typing import List
from cachedecorator import redis_cache



router = APIRouter(
    tags = ["Products"],
    prefix = "/products"
)

@router.get("/", response_model= List[Product])
@redis_cache(ttl=30, key_fields=["dfd"])
async def read_products(db: AsyncSession = Depends(get_db)):
    products = await crud.get_products(db)
    return products

@router.get("/{product_id}", response_model=Product)
@redis_cache(ttl=30, key_fields=["product_id"])
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    current_product = await crud.get_product(db, product_id)
    if not current_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return current_product

@router.post("/",response_model = Product)
async def create_product(product : ProductCreate, db: AsyncSession = Depends(get_db)):
    newproduct = await crud.create_product(db,product)
    return newproduct

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    updated = await crud.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await read_product.invalidate(func_name="read_product",
        key_fields={"product_id": product_id})

    return updated

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    deletedproduct = await crud.delete_product(db,product_id)
    if not deletedproduct:
        raise HTTPException(status_code = 404, detail = "product not found")
    
    await read_product.invalidate(func_name="read_product",
        key_fields={"product_id": product_id})
    return delete_product
    