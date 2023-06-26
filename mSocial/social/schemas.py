from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    email: EmailStr
    created_on: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_on: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class LogIn(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
