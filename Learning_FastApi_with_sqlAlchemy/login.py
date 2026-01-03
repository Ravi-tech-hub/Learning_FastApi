from fastapi import FastAPI ,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
import model,auth,crud,schema
from database import get_db

@app.post("/token")
async def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=crud.get_user_by_email(db,form_data.username)
    if not user or not auth.verify_password(form_data.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"},
        )
    acess_token=auth.create_access_token(data={"sub":user.email},expire_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token":acess_token,"token_type":"bearer"}

@app.get("/users/me",response_model=schema.UserResponse)
async def read_users_me(current_user:model.User=Depends(auth.get_current_user)):
    return current_user
    
@app.post("/posts/",response_model=schema.PostResponse)
async def create_post(post:schema.PostCreate,db:Session=Depends(get_db),current_user:model.User=Depends(auth.get_current_user)):
    return crud.create_post(db=db,post=post,user_id=current_user.id)

