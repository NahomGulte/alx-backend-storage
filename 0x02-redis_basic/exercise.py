#!/usr/bin/env python3
"""
This module defines a Cache class for storing and retrieving
data in Redis using random keys and built-in serialization.
"""

import redis
import uuid
from typing import Union, Callable, Optional


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

    def get(self,
            key: str,
            fn: Optional[Callable[[bytes], Union[str, int, float, bytes]]] = None
            ) -> Union[str, int, float, bytes, None]:
        """
        Retrieve the data associated with the given key from Redis.

        Args:
            key: The Redis key to retrieve.
            fn: Optional callable to convert the byte string result.

        Returns:
            The original data as transformed by fn, or the raw value
            if fn is None, or None if the key does not exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a UTF-8 decoded string from Redis using the given key.

        Args:
            key: The Redis key to retrieve.

        Returns:
            The decoded string value, or None if the key does not exist.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis using the given key.

        Args:
            key: The Redis key to retrieve.

        Returns:
            The integer value, or None if the key does not exist.
        """
        return self.get(key, lambda x: int(x))
