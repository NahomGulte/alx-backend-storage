import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        # Step 1: Initialize Redis client and flush DB
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis under a randomly generated key.

        Args:
            data: The data to store (str, bytes, int, or float)

        Returns:
            The key under which the data was stored (as a str)
        """
        # Step 2: Generate a random UUID key as a string
        key = str(uuid.uuid4())

        # Step 3: Store the data under that key
        self._redis.set(key, data)

        # Step 4: Return the key
        return key
