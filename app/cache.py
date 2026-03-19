"""Redis cache helper with TTL."""

import json
from typing import Any
import redis.asyncio as redis
from app.config import settings

_pool: redis.Redis | None = None


def get_redis() -> redis.Redis:
      global _pool
      if _pool is None:
                _pool = redis.from_url(settings.redis_url, decode_responses=True)
            return _pool


async def cache_get(key: str) -> Any | None:
      r = get_redis()
    val = await r.get(key)
    if val is None:
              return None
          try:
                    return json.loads(val)
except (json.JSONDecodeError, TypeError):
        return val


async def cache_set(key: str, value: Any, ttl_seconds: int = 900) -> None:
      r = get_redis()
    await r.set(key, json.dumps(value), ex=ttl_seconds)
