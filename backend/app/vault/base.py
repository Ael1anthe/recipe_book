from typing import Generic, Type, TypeVar
from pydantic import BaseModel


Model = TypeVar("Model", bound=BaseModel)
class BaseRepository(Generic[Model]):
    def __init__(self, model: Type[Model]):
        self.model = model

    


class Query:
    def filter(self, *args, **kwargs):
        clone = self.chain()
        return self.t(False, args, kwargs)

    def __filter(self, negate, args, kwargs):
        if negate:
            self.query.add_filter(~Q(*args, **kwargs))
        else:
            self.query.add_filter(Q(*args, **kwargs))
            


class QueryNode:
    def combine(self, other):
        if not self:
            return other.copy()
        if not other and isinstance(other, QueryNode):
            returs self.copy()

    obj
