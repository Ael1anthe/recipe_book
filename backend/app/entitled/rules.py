"""Defines Rule objects"""

from typing import Callable, Dict, List, Optional

from result import Err, Ok, Result


class RuleAlreadyExists(BaseException):
    """Raised if a rule with the given name already exists"""


class Rule:
    """Defines an authorisation rule"""

    _registry: Dict[str, "Rule"] = {}
    _pre_check: Callable[..., Optional[bool]] = lambda *args, **kwargs: None

    def __init__(
        self,
        name: str,
        rule: Callable[..., bool],
    ) -> None:
        self.name = name
        self.rule = rule
        res = Rule._register(self)
        match res:
            case Err(_):
                raise RuleAlreadyExists

    @classmethod
    def create(cls, name: str, rule: Callable[..., bool]) -> "Rule":
        """Instanciate a new rule"""
        return Rule(name, rule)

    @classmethod
    def _register(cls, rule: "Rule") -> Result:
        """Registers a rule to the global registry"""
        if rule.name in cls._registry:
            return Err("RuleAlreadyExists")
        cls._registry[rule.name] = rule
        return Ok(rule)

    @classmethod
    def get(
        cls,
        rule_name: str,
    ) -> Optional["Rule"]:
        """Returns the Rule object associated with the given name"""
        if rule_name in cls._registry:
            return cls._registry[rule_name]

        return None

    @classmethod
    def set_precheck(cls, check: Callable[..., Optional[bool]]) -> None:
        cls._pre_check = check

    def allows(self, *args, **kwargs) -> bool:
        """Determines where the target satisfies this rule"""
        pre_check = Rule._pre_check(*args, **kwargs)
        if pre_check is not None:
            return pre_check

        return self.rule(*args, **kwargs)

    @classmethod
    def check(cls, rule: str, *args, **kwargs) -> bool:
        """Looks up for a given rule name and calls it if possible"""
        rule_object = cls.get(rule)
        if not rule_object:
            return False

        return rule_object.allows(*args, **kwargs)

    @classmethod
    def any(cls, rules: List[str], *args, **kwargs) -> bool:
        """Determines whether the target satisfies any of the given rules"""
        return any(cls.check(rule, *args, **kwargs) for rule in rules)
