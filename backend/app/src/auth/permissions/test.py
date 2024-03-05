import pydantic
from src.auth.permissions.main import AuthorisationMixin, BasePolicy

class User(pydantic.BaseModel, AuthorisationMixin):
    login: str
    
class Post(pydantic.BaseModel):
    owner: User

class MyPolicy(BasePolicy):

    @classmethod
    @BasePolicy.rule
    def update(cls, u: User, p: Post):
        """Defines whether the user can update a given post"""
        return p.owner == u


user = User(login="mathias")
post = Post(owner=user)

res = MyPolicy.authorize("update", user, post)

