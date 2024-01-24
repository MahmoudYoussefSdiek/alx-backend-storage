#!/usr/bin/env python3
"""
Module for Web
"""
import requests
import redis
from functools import wraps

r = redis.Redis()


def count_url_calls(func):
    """
    Decorator to count how many times a URL was accessed
    """
    @wraps(func)
    def wrapper(url):
        """
        Wrapper function for the decorator
        """
        r.incr(f"count:{url}")
        return func(url)
    return wrapper

def cache_page(func):
    """
    Decorator to cache the result of get_page with an expiration time of 10 seconds
    """
    @wraps(func)
    def wrapper(url):
        """
        Wrapper function for the decorator
        """
        result = r.get(url)
        if result is None:
            result = func(url)
            r.set(url, result, ex=10)
        return result
    return wrapper

@count_url_calls
@cache_page
def get_page(url: str) -> str:
    """
    Function to get the HTML content of a URL
    """
    response = requests.get(url)
    return response.text
