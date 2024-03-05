import typing
import result


class BasePolicy:
    """Base class for defining policies"""

    _registry: dict[str, typing.Callable[..., bool]] = {}

    @classmethod
    def rule(
        cls, decorated: typing.Callable[..., bool], label: typing.Optional[str] = None
    ) -> typing.Callable[..., bool]:
        """Register a given function as a rule for this policy"""
        _label = label if label else decorated.__name__
        if not _label in cls._registry:
            cls._registry[_label] = decorated
        return decorated

    @classmethod
    def authorize(cls, rule: str, *args, **kwargs) -> result.Result[bool, str]:
        """Looks up a given rule and applies it to the given parameter"""
        if rule in cls._registry:
            return result.Ok(cls._registry[rule](cls, *args, **kwargs))

        return result.Err("Rule does not exist")