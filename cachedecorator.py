import hashlib
import functools
import pickle
import aioredis
from typing import Callable
from inspect import signature

redis_client =aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=False)

def make_cache_key(func, key_fields, args, kwargs):
    bound_args = signature(func).bind(*args, **kwargs)
    bound_args.apply_defaults()
    arguments = bound_args.arguments

    relevant_args = {k: arguments[k] for k in key_fields if k in arguments}

    raw_key = f"{func.__module__}:{func.__name__}:{relevant_args}"
    
    key = hashlib.sha256(raw_key.encode()).hexdigest()
    return key


def redis_cache(ttl:int = 30, key_fields: list[str] = None):
    def decorator(func:callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
        
            cache_key = make_cache_key(func, key_fields, args, kwargs)
            print(cache_key)
            cached_result = await redis_client.get(cache_key)
            if cached_result:
                return pickle.loads(cached_result)
            result = await func(*args, **kwargs)
            await redis_client.setex(cache_key, ttl, pickle.dumps(result))

            return result
        
        async def invalidate(func_name: str, key_fields: dict):
            raw_key = f"{func.__module__}:{func_name}:{key_fields}"
            key = hashlib.sha256(raw_key.encode()).hexdigest()
            
            await redis_client.delete(key)
            
        wrapper.invalidate = invalidate    
        return wrapper
    return decorator