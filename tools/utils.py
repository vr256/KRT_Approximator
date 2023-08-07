import json
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


def load_locale(path):
    # * to avoid circular imports
    from tools.config import AppState

    with open(AppState.lang, "r", encoding="utf-8") as file:
        loc = json.load(file)[path]
        return loc
