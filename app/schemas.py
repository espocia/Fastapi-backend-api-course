from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# BaseModels
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


# Post Schemas
class PostCreate(PostBase):
    pass


class Post(PostBase):
    create_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


# User Schemas
class User(UserBase):
    pass

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    id: Optional[str] = None
