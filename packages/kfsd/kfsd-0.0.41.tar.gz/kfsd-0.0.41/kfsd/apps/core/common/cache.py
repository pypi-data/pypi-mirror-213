from django.core.cache import cache as DjangoCache
from functools import wraps


def cache(key):
    def get(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = DjangoCache.get(key)
            if data is None:
                data = func(*args, **kwargs)
                DjangoCache.set(key, data, timeout=3600)
            return data

        return wrapper

    return get
