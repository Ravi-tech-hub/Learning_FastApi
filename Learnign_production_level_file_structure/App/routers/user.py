from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud,schema
from dependecies import get_db

router=APIRouter(prefix="/users",tags=["users"],responses={404:{"description":"Not found"}})
@router.get("/",response_model=List[schema.UserResponse])
def read_users(skip:int=0,limit:int=10,db:Session=Depends(get_db)):
  return crud.get_users(db,skip=skip,limit=limit)

@router.get("/{user_id}",response_model=schema.UserResponse)
def read_user(user_id:int,db:Session=Depends(get_db)):
  user=crud.get_user(db,user_id=user_id)
  if user is None:
    raise HTTPException(status_code=404,detail="User not found")
  return user

