import pydantic
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class InvalidTitleError(Exception):
    def __init__(self, value: str, message: str):
        self.value = value
        self.message = message
        super().__init__(message)

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

    @pydantic.validator("title")
    @classmethod
    def validTitle(cls, value: str):
        if value[0].islower(): raise InvalidTitleError(
                value = value,
                message = "Title must begin with Capital Letter")
        return value
    
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    creator: UserResponse
    class Config:
        orm_mode = True

class PostOutput(BaseModel):
    Post: PostResponse
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class VotePost(BaseModel):
    post_id: int
    vote_direction: Literal[0,1]