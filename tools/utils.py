from functools import wraps


def singleton(cls):
    obj = None

    @wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal obj
        if obj is None:
            obj = cls(*args, **kwargs)
        return obj
    return wrapper
