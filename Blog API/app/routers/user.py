from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schema.user import UserCreate,UserResponse
from app.crud.user import create_user

router=APIRouter()

@router.post("/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    new_user=create_user(db,user)
    return new_user