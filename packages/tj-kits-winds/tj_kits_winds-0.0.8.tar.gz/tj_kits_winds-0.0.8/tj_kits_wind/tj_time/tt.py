from pydantic import BaseModel

__all__ = ['get_user']


class User(BaseModel):
    name: str
    age: int


def get_user():
    return User(name="Peter", age=123)
