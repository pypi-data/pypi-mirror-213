"""A function that can be decorated or wrapped around a file"""
import functools
import inspect
import types
from typing import Callable

from .cfg_dict import CfgDict


def copy_func(f, name=None):
    """
    return a function with same code, globals, defaults, closure, and
    name (or provide a new name)
    """
    fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__, f.__defaults__, f.__closure__)
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)
    fn.__annotations__ = f.__annotations__
    fn.__doc__ = f.__doc__
    return fn


def wrap_config(cfg_dict: CfgDict) -> Callable[..., Callable]:
    """Wraps a function with a CfgDict file to make an easy config configuration"""

    def _wrapper(func: Callable) -> Callable:
        # get parameters and defaults

        parameters: dict[str, inspect.Parameter] = dict(inspect.signature(func).parameters)
        save_after = False
        for name, param in parameters.items():
            if name not in cfg_dict:
                if cfg_dict.is_serializable(param.default):
                    save_after = True
                    cfg_dict[name] = param.default
        if save_after:
            cfg_dict.save()
        new_defaults = dict(zip(parameters.keys(), map(lambda x: x.default, parameters.values())))
        new_defaults.update({k: v for k, v in cfg_dict.items() if k in new_defaults})

        func = copy_func(func)

        @functools.wraps(func)
        def _wrap(*args, **kwargs):
            new_defaults = dict(zip(parameters.keys(), map(lambda x: x.default, parameters.values())))
            new_defaults.update({k: v for k, v in cfg_dict.items() if k in new_defaults})
            new_defaults.update(kwargs)

            # convert args to kwargs
            default_lst = list(enumerate(new_defaults.items()))
            for idx, arg in enumerate(args):
                default_lst[idx] = (default_lst[idx][0], (default_lst[idx][1][0], arg))
            new_defaults = dict(map(lambda arg: arg[1], default_lst))
            return func(**new_defaults)  # type: ignore

        _wrap.__wrapped__.__defaults__ = tuple(new_defaults.values())  # type: ignore

        return _wrap

    return _wrapper
