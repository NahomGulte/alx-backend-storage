#!/usr/bin/env python3
"""
This module defines a Cache class for storing and retrieving
data in Redis using random keys and built-in serialization.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class provides methods to interact with Redis for
    temporary storage using randomly generated keys.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache instance by connecting to Redis and
        clearing any existing data in the current Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis under a randomly generated key.

        Args:
            data: A str, bytes, int, or float to store in the Redis cache.

        Returns:
            A string key under which the data was stored in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
