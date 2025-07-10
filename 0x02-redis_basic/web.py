#!/usr/bin/env python3
"""
This module defines get_page which fetches and caches HTML
content from a given URL using Redis, and counts accesses.
"""

import redis
import requests


r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetch the HTML content of the given URL. Cache it in Redis
    for 10 seconds and track the number of times this URL has
    been accessed using the key 'count:{url}'.

    Args:
        url (str): The target URL.

    Returns:
        str: The HTML content of the response.
    """
    # Check if page is cached
    cached = r.get(url)
    if cached:
        return cached.decode('utf-8')

    # Not cached, so increment the counter
    r.incr(f"count:{url}")

    # Fetch the page
    response = requests.get(url)
    content = response.text

    # Cache it with 10-second expiration
