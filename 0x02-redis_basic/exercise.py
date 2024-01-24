#!/usr/bin/env python3
"""
Module for Cache
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times methods of the Cache class are called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorator
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Cache class
    """
    def __init__(self):
        """
        Initialize
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Get the value of a key and optional conversion of the value
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Get the value of a key and convert it to a string
        """
        value = self.get(key, fn=lambda x: x.decode("utf-8"))
        return value

    def get_int(self, key: str) -> int:
        """
        Get the value of a key and convert it to an integer
        """
        value = self.get(key, fn=int)
        return value
