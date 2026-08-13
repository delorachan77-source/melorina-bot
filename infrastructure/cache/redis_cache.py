from typing import Optional
from django.core.cache import cache
from core.interfaces.cache import ICache

class RedisCache(ICache):
    def get(self, key: str) -> Optional[str]:
        return cache.get(key)
    
    def set(self, key: str, value: str, ttl: int = 3600) -> bool:
        cache.set(key, value, timeout=ttl)
        return True
    
    def delete(self, key: str) -> bool:
        cache.delete(key)
        return True
    
    def exists(self, key: str) -> bool:
        return cache.has_key(key) if hasattr(cache, 'has_key') else bool(cache.get(key))
