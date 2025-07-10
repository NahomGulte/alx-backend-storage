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


def cache_result(exp_
