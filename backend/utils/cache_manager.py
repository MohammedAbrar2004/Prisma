"""
PRISMA Cache Manager

Lightweight caching system for API responses and computed data.

Features:
- Time-based TTL (Time To Live) expiration
- Simple file-based storage (JSON)
- Rate-limit protection for external APIs
- Automatic cache invalidation

Design:
- Store cache in backend/.cache/ directory
- Each cache entry has: data, timestamp, ttl
- Cache keys are hashed for filesystem safety

Usage:
    from utils.cache_manager import CacheManager
    
    cache = CacheManager()
    
    # Try to get cached data
    data = cache.get("api_response_key")
    if data is None:
        # Make API call
        data = fetch_from_api()
        # Cache for 24 hours
        cache.set("api_response_key", data, ttl=86400)
"""

import os
import json
import hashlib
from typing import Any, Optional
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================================
# Configuration
# ============================================================================

# Default cache directory
CACHE_DIR = Path(__file__).parent.parent / ".cache"

# Default TTL values (in seconds)
DEFAULT_TTL = 86400  # 24 hours
SHORT_TTL = 3600     # 1 hour
LONG_TTL = 604800    # 7 days

# Cache enabled flag (can disable for testing)
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"


# ============================================================================
# Cache Manager
# ============================================================================

class CacheManager:
    """
    Simple file-based cache manager with TTL support.
    
    Attributes:
        cache_dir: Directory where cache files are stored
        enabled: Whether caching is enabled
    
    Example:
        >>> cache = CacheManager()
        >>> cache.set("my_key", {"data": "value"}, ttl=3600)
        >>> data = cache.get("my_key")
        >>> print(data)
        {"data": "value"}
    """
    
    def __init__(self, cache_dir: Optional[Path] = None, enabled: bool = CACHE_ENABLED):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Custom cache directory (defaults to backend/.cache/)
            enabled: Whether caching is enabled
        """
        self.cache_dir = cache_dir or CACHE_DIR
        self.enabled = enabled
        
        # Create cache directory if it doesn't exist
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> Path:
        """
        Get the file path for a cache key.
        
        Args:
            key: Cache key
        
        Returns:
            Path to cache file
        """
        # Hash the key to create a safe filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get cached data if it exists and hasn't expired.
        
        Args:
            key: Cache key
        
        Returns:
            Cached data if valid, None otherwise
        
        Example:
            >>> cache = CacheManager()
            >>> data = cache.get("commodity_prices_2025-11-08")
            >>> if data is None:
            ...     data = fetch_prices()
            ...     cache.set("commodity_prices_2025-11-08", data)
        """
        if not self.enabled:
            return None
        
        cache_path = self._get_cache_path(key)
        
        # Check if cache file exists
        if not cache_path.exists():
            return None
        
        try:
            # Read cache file
            with open(cache_path, 'r') as f:
                cache_entry = json.load(f)
            
            # Check expiration
            created_at = datetime.fromisoformat(cache_entry["timestamp"])
            ttl = cache_entry.get("ttl", DEFAULT_TTL)
            expires_at = created_at + timedelta(seconds=ttl)
            
            if datetime.now() > expires_at:
                # Cache expired - delete it
                cache_path.unlink()
                return None
            
            # Return cached data
            return cache_entry["data"]
        
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Corrupted cache file - delete it
            print(f"Cache error for key '{key}': {e}")
            cache_path.unlink(missing_ok=True)
            return None
    
    def set(self, key: str, data: Any, ttl: int = DEFAULT_TTL) -> bool:
        """
        Store data in cache with TTL.
        
        Args:
            key: Cache key
            data: Data to cache (must be JSON-serializable)
            ttl: Time to live in seconds (default: 24 hours)
        
        Returns:
            True if cached successfully, False otherwise
        
        Example:
            >>> cache = CacheManager()
            >>> cache.set("api_response", {"value": 42}, ttl=3600)
            True
        """
        if not self.enabled:
            return False
        
        cache_path = self._get_cache_path(key)
        
        try:
            cache_entry = {
                "key": key,  # Store original key for debugging
                "data": data,
                "timestamp": datetime.now().isoformat(),
                "ttl": ttl
            }
            
            # Write cache file
            with open(cache_path, 'w') as f:
                json.dump(cache_entry, f, indent=2)
            
            return True
        
        except (TypeError, ValueError) as e:
            print(f"Failed to cache data for key '{key}': {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete cached data for a specific key.
        
        Args:
            key: Cache key
        
        Returns:
            True if deleted, False if not found
        """
        if not self.enabled:
            return False
        
        cache_path = self._get_cache_path(key)
        
        if cache_path.exists():
            cache_path.unlink()
            return True
        
        return False
    
    def clear_all(self) -> int:
        """
        Clear all cached data.
        
        Returns:
            Number of cache files deleted
        
        Example:
            >>> cache = CacheManager()
            >>> count = cache.clear_all()
            >>> print(f"Cleared {count} cache entries")
        """
        if not self.enabled or not self.cache_dir.exists():
            return 0
        
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        
        return count
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        
        Example:
            >>> cache = CacheManager()
            >>> stats = cache.get_stats()
            >>> print(f"Cache size: {stats['total_entries']} entries")
        """
        if not self.enabled or not self.cache_dir.exists():
            return {
                "enabled": False,
                "total_entries": 0,
                "total_size_bytes": 0
            }
        
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            "enabled": True,
            "cache_dir": str(self.cache_dir),
            "total_entries": len(cache_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }


# ============================================================================
# Convenience Functions
# ============================================================================

# Global cache instance
_global_cache = CacheManager()


def get_cached(key: str) -> Optional[Any]:
    """
    Get cached data using global cache instance.
    
    Convenience function for quick access.
    """
    return _global_cache.get(key)


def set_cached(key: str, data: Any, ttl: int = DEFAULT_TTL) -> bool:
    """
    Cache data using global cache instance.
    
    Convenience function for quick caching.
    """
    return _global_cache.set(key, data, ttl)


def clear_cache() -> int:
    """
    Clear all cached data using global cache instance.
    """
    return _global_cache.clear_all()


def cache_stats() -> dict:
    """
    Get cache statistics using global cache instance.
    """
    return _global_cache.get_stats()


# ============================================================================
# Decorator for Automatic Caching
# ============================================================================

def cached(key_prefix: str, ttl: int = DEFAULT_TTL):
    """
    Decorator for automatic function result caching.
    
    Args:
        key_prefix: Prefix for cache key
        ttl: Time to live in seconds
    
    Example:
        >>> @cached("api_response", ttl=3600)
        ... def fetch_data(param1, param2):
        ...     return expensive_api_call(param1, param2)
        
        >>> # First call - fetches from API and caches
        >>> data = fetch_data("a", "b")
        
        >>> # Second call - returns cached data
        >>> data = fetch_data("a", "b")
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Build cache key from function args
            args_str = "_".join(str(arg) for arg in args)
            kwargs_str = "_".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = f"{key_prefix}:{func.__name__}:{args_str}:{kwargs_str}"
            
            # Try to get cached result
            cached_result = get_cached(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            set_cached(cache_key, result, ttl=ttl)
            
            return result
        
        return wrapper
    return decorator


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "CacheManager",
    "get_cached",
    "set_cached",
    "clear_cache",
    "cache_stats",
    "cached",
    "DEFAULT_TTL",
    "SHORT_TTL",
    "LONG_TTL",
]

