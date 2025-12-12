from pydantic import BaseModel,Field,EmailStr
from typing import Optional
from datetime import datetime

# request model
class UserCreate(BaseModel):
  username:str=Field(...,min_length=3,max_length=50)
  email:EmailStr
  password:str=Field(...,min_length=6)
  full_name:Optional[str]=None

# response model
class UserResponse(BaseModel):  
  id:int
  username:str
  email:str
  full_name:Optional[str]
  created_at:datetime
  class Config:form_attributes = True
 

from fastapi import FastAPI
app=FastAPI()
user_db=[]

@app.post("/users/",response_model=UserResponse)
def create_user(user:UserCreate):
  new_user={
    "id":len(user_db)+1,
    "username":user.username,
    "email":user.email,
    "full_name":user.full_name,
    "created_at":datetime.now()
  }
  user_db.append(new_user)
  return new_user

# get with response model

@app.get("/users/{user_id}",response_model=UserResponse)
def get_user(user_id:int):
  for user in user_db:
    if user["id"]==user_id:
      return user