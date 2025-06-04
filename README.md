- 🧠FastAPI + Redis Caching with Decorator

  This project is a simple Product Management REST API built with FastAPI and PostgreSQL, enhanced with Redis caching to improve response time and   reduce database load. It demonstrates how to use a custom async decorator to handle cache logic cleanly.

- ⚙️Technologies Used:
  FastAPI
  SQLAlchemy (Async)
  PostgreSQL
  Redis
  aioredis


- 🚀Features:
  Full CRUD API for products
  Custom decorator for automatic response caching
  Support for manual cache invalidation on data updates
  Smart cache key generation using selected function arguments
  Configurable TTL (Time-To-Live) for cached entries


- 💡How It Works
   @redis_cache Decorator
   Use the decorator to cache the output of any async function. You can specify which arguments should be used to build the cache key.

   @redis_cache(ttl=60, key_fields=["product_id"])
    async def read_product(product_id: int):
    ...
  
- Cache Invalidation: 
     When the underlying data changes (e.g., in an update), invalidate the cache manually to prevent stale data:
     await read_product.invalidate("read_product", {"product_id": product_id})


- 🔐How Cache Keys Are Generated: 
    Cache keys are generated using the function’s module, name, and specified key_fields. This is converted to a string and hashed using SHA256  for    uniqueness and safety:
    app.module:function_name:{'product_id': 3}
↓
SHA256 hash → Redis cache key

- 📦Project Structure : 
app/
│
├── db/
    └── database.py
│   └── model.py
        # SQLAlchemy models
└── routers
    └── router.py
├── operations
  └── crud.py              # Database interaction logic
├── cache_decorator.py   # Redis caching logic (with invalidate support)
└── main.py   
├── schema.py            # Pydantic schemas

- 🐳Docker Support: 
   You can easily run the project and Redis with Docker:
   services:
     redis:
       image: redis:latest
       ports:
        - "6379:6379"
