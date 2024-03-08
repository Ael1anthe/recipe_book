import typing

import result

from entitled import rules


class PolicyMeta(type):
    def __new__(mcs, name, bases, dct):
        dct["_registry"] = set()
        return super().__new__(mcs, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        for attr_name in dct:
            attr = getattr(cls, attr_name)
            if callable(attr) and hasattr(attr, "_registerable"):
                rules.Rule.create(f"{cls.__name__}.{attr_name}", attr)
                cls.__dict__["_registry"].add(attr_name)


class Policy(metaclass=PolicyMeta):
    """Base class for defining policies"""

    @classmethod
    def register(cls, func: typing.Callable):
        setattr(func, "_registerable", True)
        return func

    @classmethod
    def authorize(cls, rule: str, *args, **kwargs) -> result.Result[bool, str]:
        """Looks up a given rule and applies it to the given parameter"""
        if rule in cls.__dict__["_registry"]:
            return result.Ok(
                rules.Rule.check(f"{cls.__name__}.{rule}", *args, **kwargs)
            )

        return result.Err("Rule does not exist")
