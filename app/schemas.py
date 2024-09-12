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
 
# Post Schemas
class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    create_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


