from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:zr123456@localhost:5432/postgres"
engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, class_= AsyncSession, expire_on_commit= False)

Base = declarative_base()

                  

async def get_db():
    async with SessionLocal() as session:
       yield session