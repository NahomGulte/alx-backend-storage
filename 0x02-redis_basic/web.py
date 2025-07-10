#!/usr/bin/env python3
"""
This module implements a caching and access-counting system
for web pages using Redis. It caches page content and tracks
access frequency with expiration.
"""

import redis
import requests
from typing import Callable
from functools import wraps


# Redis connection (default localhost:6379)
r = redis.Redis()


def count_url_access(fn: Callable) -> Callable:
    """
    Decorator that increments a Redis counter every time
    a URL is accessed through the decorated function.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        r.incr(f"count:{url}")
        return fn(url)
    return wrapper


def cache_result(expiration: int = 10) -> Callable:
    """
    Decorator that caches the result of a URL fetch in Redis
    and reuses it if it's still valid.
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(url: str) -> str:
            cached = r.get(url)
            if cached:
                return cached.decode('utf-8')

            # Fetch and cache if not found
            result = fn(url)
            r.setex(url, expiration, result)
            return result
        return wrapper
    return decorator


@count_url_access
@cache_result(expiration=10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of the specified URL.

    Args:
        url: A full HTTP/HTTPS URL.

    Returns:
        The raw HTML content as a string.
    """
    response = requests.get(url)
    return response.text
