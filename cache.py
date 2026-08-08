import redis
import os
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

r = redis.from_url(REDIS_URL, decode_responses=True)

def get_cache(key: str):
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value, expire=300):
    r.setex(key, expire, json.dumps(value))

def delete_cache(key: str):
    r.delete(key)
