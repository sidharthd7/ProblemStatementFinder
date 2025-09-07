from redis import Redis
from typing import Optional, Any
import json
from .config import settings
from .logging import logger

class RedisCache:
    def __init__(self):
        self.redis_client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        logger.info("Redis cache initialized")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {str(e)}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: int = settings.CACHE_EXPIRE_SECONDS
    ) -> bool:
        """Set value in cache with expiration"""
        try:
            serialized_value = json.dumps(value)
            return self.redis_client.setex(
                key,
                expire,
                serialized_value
            )
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {str(e)}")
            return False

    async def clear_pattern(self, pattern: str) -> bool:
        """Clear all keys matching pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return bool(self.redis_client.delete(*keys))
            return True
        except Exception as e:
            logger.error(f"Error clearing cache pattern {pattern}: {str(e)}")
            return False

# Initialize cache
# cache = RedisCache() 