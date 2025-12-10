"""
Core application components
"""
from static_memory_cache import StaticMemoryCache

# Re-export for backward compatibility
Settings = StaticMemoryCache
get_settings = lambda: StaticMemoryCache

__all__ = ["Settings", "get_settings"]
