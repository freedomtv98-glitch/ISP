"""Caching layer using Redis."""

import logging
import json
from typing import Any, Optional
from datetime import timedelta

logger = logging.getLogger(__name__)


class CacheManager:
    """Redis-based cache manager."""

    def __init__(self, redis_client):
        """Initialize cache manager.
        
        Args:
            redis_client: Redis client instance
        """
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set cache value.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
        """
        try:
            if ttl is None:
                ttl = self.default_ttl
            
            serialized = json.dumps(value)
            self.redis.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    async def get(self, key: str) -> Optional[Any]:
        """Get cache value.
        
        Args:
            key: Cache key
        """
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    async def delete(self, key: str) -> bool:
        """Delete cache value.
        
        Args:
            key: Cache key
        """
        try:
            self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    async def clear(self) -> bool:
        """Clear all cache."""
        try:
            self.redis.flushdb()
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
