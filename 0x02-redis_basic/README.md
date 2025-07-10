# Redis Cache Module

This project provides a `Cache` class that connects to a Redis database and allows storing values under automatically generated random keys. It supports values of type `str`, `bytes`, `int`, and `float`.

## Usage

```python
from cache import Cache

cache = Cache()
key = cache.store("hello")
print("Stored under:", key)
