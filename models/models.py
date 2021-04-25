from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int = None
    email: str
    password: str
    first_name: str
    last_name: str
    is_registered: bool = False


class Post(BaseModel):
    id: int = None
    title: str
    text: str
    author: int = None


class BatchPosts(BaseModel):
    limit: int
    offset: int
    post_numbers: List[int]
