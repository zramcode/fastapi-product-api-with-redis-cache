import asyncio
from app.db.database import engine

async def test_connection():
    async with engine.begin() as conn:
        await conn.execute("SELECT 1")
    print("DB connected")

asyncio.run(test_connection())