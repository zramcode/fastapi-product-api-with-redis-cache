from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import  select
from app.db import model
from app.schema import Product, ProductCreate,ProductUpdate

async def get_product(db: AsyncSession, product_id: int):
   result = await db.execute(select(model.Product).where(model.Product.id == product_id))
   return result.scalar_one_or_none()

async def get_products(db: AsyncSession):
   result = await db.execute(select(model.Product))
   return result.scalars().all()

async def create_product(db: AsyncSession, product:ProductCreate):
    db_product = model.Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def update_product(db:AsyncSession, product_id: int, product: ProductUpdate):
   current_product = await get_product(db, product_id)
   if not current_product:
      return None
   
   for key,value in product.model_dump().items():
      setattr(current_product, key, value)
   await db.commit()
   await db.refresh(current_product)
   return current_product

async def delete_product(db:AsyncSession, product_id: int):
   current_product = await get_product(db, product_id)
   if not current_product:
      return None
   await db.delete(current_product)
   await db.commit()
   return current_product

   