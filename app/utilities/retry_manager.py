"""
Retry Manager

Manages retry logic for failed operations.
"""

import asyncio
from typing import Callable, Any, Optional
from functools import wraps

from app.telemetries.logger import logger


class RetryManager:
    """
    Manages retry logic with exponential backoff
    """
    
    @staticmethod
    async def retry_async(
        func: Callable,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        exceptions: tuple = (Exception,)
    ) -> Any:
        """
        Retry an async function with exponential backoff
        
        Args:
            func: Async function to retry
            max_attempts: Maximum number of attempts
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff
            exceptions: Tuple of exceptions to catch
            
        Returns:
            Function result
            
        Raises:
            Last exception if all attempts fail
        """
        last_exception = None
        
        for attempt in range(1, max_attempts + 1):
            try:
                return await func()
            except exceptions as e:
                last_exception = e
                
                if attempt == max_attempts:
                    logger.error(f"All {max_attempts} retry attempts failed")
                    raise
                
                delay = min(base_delay * (exponential_base ** (attempt - 1)), max_delay)
                logger.warning(f"Attempt {attempt}/{max_attempts} failed: {e}. Retrying in {delay}s...")
                
                await asyncio.sleep(delay)
        
        raise last_exception
    
    @staticmethod
    def retry_sync(
        func: Callable,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        exceptions: tuple = (Exception,)
    ) -> Any:
        """
        Retry a sync function with exponential backoff
        
        Args:
            func: Function to retry
            max_attempts: Maximum number of attempts
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff
            exceptions: Tuple of exceptions to catch
            
        Returns:
            Function result
            
        Raises:
            Last exception if all attempts fail
        """
        import time
        
        last_exception = None
        
        for attempt in range(1, max_attempts + 1):
            try:
                return func()
            except exceptions as e:
                last_exception = e
                
                if attempt == max_attempts:
                    logger.error(f"All {max_attempts} retry attempts failed")
                    raise
                
                delay = min(base_delay * (exponential_base ** (attempt - 1)), max_delay)
                logger.warning(f"Attempt {attempt}/{max_attempts} failed: {e}. Retrying in {delay}s...")
                
                time.sleep(delay)
        
        raise last_exception


def with_retry(max_attempts: int = 3, base_delay: float = 1.0):
    """
    Decorator for adding retry logic to async functions
    
    Args:
        max_attempts: Maximum number of attempts
        base_delay: Base delay in seconds
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await RetryManager.retry_async(
                lambda: func(*args, **kwargs),
                max_attempts=max_attempts,
                base_delay=base_delay
            )
        return wrapper
    return decorator
