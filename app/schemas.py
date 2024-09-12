from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


# BaseModels
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserBase(BaseModel):
    email: EmailStr
    phone_number: str
    password: str

# User Schemas
class User(UserBase):
    pass

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime

    class Config:
        from_attributes = True


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
        from_attributes = True

class PostVotesResponse(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        from_attributes = True

# Votes Schemas
class VoteBase(BaseModel):
    user_id: int
    post_id: int
    
class VoteIn(BaseModel):
    post_id: int
    vote_dir:conint(ge=0, le=1)


class VoteOut(VoteBase):
    pass
    class Config:
        from_attributes = True
