from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    email:EmailStr
    username:str
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    username:str

    class config:
        from_attributes=True

