from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
import model
import schema
import crud
from database import engine,get_db

model.Base.metadata.create_all(bind=engine)

app=FastAPI(title="Blog Api")

@app.post("/users/",response_model=schema.UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user:schema.UserCreate,db:Session=Depends(get_db)):
  existing_user=crud.get_user_by_email(db,email=user.email)
  if existing_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registred")
  return crud.create_user(db,user=user)

@app.get("/users/",response_model=list[schema.UserResponse])
def read_users(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
  return crud.get_users(db,skip=skip,limit=limit)

@app.get("/users/{user_id}",response_model=schema.UserWithPosts)
def read_user(user_id:int,db:Session=Depends(get_db)):
  user=crud.get_user(db,user_id=user_id)
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
  return user

@app.post("/users/{user_id}/posts/",response_model=schema.PostResponse)
def create_post_for_user(user_id:int,post:schema.PostCreate,db:Session=Depends(get_db)):
  return crud.create_post(db,post=post,user_id=user_id)


@app.get("/posts/",response_model=list[schema.PostResponse])
def read_posts(skip: int = 0,limit: int = 100,db: Session = Depends(get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)
