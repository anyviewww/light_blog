from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True

class ArticleBase(BaseModel):
    title: str
    content: str

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    article_id: int

class Comment(CommentBase):
    id: int
    article_id: int
    user_id: int

    class Config:
        from_attributes = True