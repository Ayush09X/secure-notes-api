import redis
import os
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    r = redis.from_url(REDIS_URL, decode_responses=True)
    r.ping()  # Test connection
except Exception:
    r = None  # Redis unavailable, skip caching

def get_cache(key: str):
    if not r:
        return None
    try:
        data = r.get(key)
        if data:
            return json.loads(data)
    except Exception:
        pass
    return None

def set_cache(key: str, value, expire=300):
    if not r:
        return
    try:
        r.setex(key, expire, json.dumps(value))
    except Exception:
        pass

def delete_cache(key: str):
    if not r:
        return
    try:
        r.delete(key)
    except Exception:
        pass