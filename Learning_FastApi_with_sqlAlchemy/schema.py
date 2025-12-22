from pydantic import BaseModel,EmailStr
from typing import Optional,List
from datetime import datetime
# pydantic schema:- A schema:-Validates incoming request data,Controls outgoing response data,Talks to API
class UserBase(BaseModel):
  email:EmailStr
  username:str

class UserCreate(UserBase):
  password:str

class UserResponse(UserBase):
  id:int
  is_active:bool
  created_at:datetime
  class Config:
    from_attributes = True

class PostBase(BaseModel):
   title:str
   content:str

class PostCreate(PostBase):
   pass

class PostResponse(PostBase):
   id:int
   user_id:int
   created_at:datetime
   class Config:
      from_attributes = True


class UserWithPosts(UserResponse):
    posts: List[PostResponse] = []