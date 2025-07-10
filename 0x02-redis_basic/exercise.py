#!/usr/bin/env python3
"""
This module defines a Cache class for storing and retrieving
data in Redis using random keys. It includes tracking of method
call counts and input/output history using Redis lists and counters.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.

    Uses Redis INCR to increment a counter stored under the method's
    qualified name (e.g., 'Cache.store').
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs
    for a method in Redis lists.

    Stores inputs in 'method_name:inputs' and outputs in 'method_name:outputs'.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store input arguments as string
        self._redis.rpush(input_key, str(args))

        # Call the actual method
        result = method(self, *args, **kwargs)

        # Store output
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper


def replay(method: Callable) -> None:
    """
    Display the call history (inputs and outputs) of a method
    recorded by the call_history decorator.

    Args:
        method: The method to replay.
    """
    r = redis.Redis()
    name = method.__qualname__

    inputs_key = f"{name}:inputs"
    outputs_key = f"{name}:outputs"

    inputs = r.lrange(inputs_key, 0, -1)
    outputs = r.lrange(outputs_key, 0, -1)

    call_count = len(inputs)
    print(f"{name} was called {call_count} times:")

    for inp, outp in zip(inputs, outputs):
        print(f"{name}(*{inp.decode('utf-8')}) -> {outp.decode('utf-8')}")


class Cache:
    """
    Cache class provides methods to interact with Redis for
    temporary storage using randomly generated keys. It also
    supports call count tracking and input/output history logging.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache instance by connecting to Redis and
        clearing any existing data in the current Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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

    def get(
        self,
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
