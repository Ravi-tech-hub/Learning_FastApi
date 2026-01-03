from datetime import datetime,timedelta
from typing import Optional
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import model
from database import get_db

SECRET_KEY="a24ac94ccd124604ba843ca8b0f55f8cccb924e5c3997a35b0f0a72d335cee96"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30 

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data:dict,expire_delta:Optional[timedelta]=None):
    to_encode=data.copy()
    expire=datetime.utcnow()+(expire_delta or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if email is None:
          raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    
    user=db.query(model.User).filter(model.User.email==email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


    