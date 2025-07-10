#!/usr/bin/env python3
"""
This module defines a get_page function that retrieves and
caches a web page's content using Redis, and counts how many
times a particular URL has been accessed.
"""

import redis
import requests

r = redis.Redis()


def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL, using Redis to cache
    the result for 10 seconds and to count how many times
    the URL was accessed.

    Args:
        url: A string containing the URL to fetch.

    Returns:
        The HTML content as a string.
    """
    cached_content = r.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    # Increment access count
    r.incr(f"count:{url}")

    # Fetch and cache
    response = requests.get(url)
    content = response.text
    r.setex(url, 10, content)

    return content
