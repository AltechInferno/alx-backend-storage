#!/usr/bin/env python3
""" client module
"""
import redis
from uuid import uuid4
from functools import wraps
from typing import Any, Callable, Optional, Union

def replay(fn: Callable) -> None:
    """ number of times a function was called and display:
            - number of times it was called
            - args and output for each call
    """
    clt = redis.Redis()
    calls = clt.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              clt.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               clt.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


def call_history(method: Callable) -> Callable:
    """ Cache class method to track args
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """ tracks its passed argument by storing
            them to redis
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper

def count_calls(method: Callable) -> Callable:
    """ Cache class methods to track call count
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """ adds its call count redis before execution
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ Caching class
    """
    def __init__(self) -> None:
        """ Init new cache object
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """ Saves data in redis with randomly generated key
        """
        key = str(uuid4())
        clt = self._redis
        clt.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """ converts result byte  into correct data type
        """
        clt = self._redis
        value = clt.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, data: bytes) -> str:
        """ bytes to string
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """ bytes to integers
        """
        return int(data)
