from typing import Any, Callable, Dict, List, Optional


class Authorizable:
    pass


class Rule:
    _registry: Dict[str, "Rule"]

    def __init__(
        self,
        name: str,
        rule: Callable[..., bool],
    ) -> None:
        self.name = name
        self.rule = rule
        self._registry[self.name] = self

    def allows(
        self,
        target: Authorizable,
        model: Optional[Any] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Determines where the target satisfies this rule"""
        return self.rule(target, model, context)

    @classmethod
    def get(
        cls,
        rule_name: str,
    ) -> Optional["Rule"]:
        """Returns the Rule object associated with the given name"""
        if rule_name in cls._registry.keys():
            return cls._registry[rule_name]

        return None

    @classmethod
    def check(
        cls,
        rule: str,
        target: Authorizable,
        model: Optional[Any] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Looks up for a given rule name and calls it if possible"""
        rule_object = cls.get(rule)
        if not rule_object:
            return False

        return rule_object.allows(target, model, context)

    @classmethod
    def any(
        cls,
        rules: List[str],
        target: Authorizable,
        model: Optional[Any] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Determines whether the target satisfies any of the given rules"""
        return any(cls.check(rule, target, model, context) for rule in rules)
