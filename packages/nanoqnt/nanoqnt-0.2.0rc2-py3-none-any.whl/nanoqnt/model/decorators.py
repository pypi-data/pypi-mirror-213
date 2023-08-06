from functools import wraps

from .exceptions import NoData


def data_not_none(func):
    @wraps
    def func(*args, **kwargs):
        if getattr(args[0], 'data', None) is None:
            raise NoData('Data not yet defined')
        return func(args, kwargs)

    return func
