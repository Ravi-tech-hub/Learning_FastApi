from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schema.user import UserCreate
from app.database.session import get_db
from models.user import User
from app.core.security import verify_password ,hash_password,create_access_token

router=APIRouter()
@router.post("/register")
def register(user:UserCreate,db:Session=Depends(get_db)):
    new_user=User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"User registerd Successfully"}

@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==form_data.username).first()
    if not user or not verify_password(form_data.password,user.hashed_password):
        return {"error":"invalid Credentials"}
    token=create_access_token({"sub":user.username})
    return {"access_token":token,"token_type":"bearer"}

