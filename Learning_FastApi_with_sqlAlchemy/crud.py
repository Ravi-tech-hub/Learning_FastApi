from sqlalchemy.orm import Session
import model
import schema
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_user(db:Session,user_id:int):
  return db.query(model.User).filter(model.User.id==user_id).first()

def get_user_by_email(db:Session,email:str):
  return db.query(model.User).filter(model.User.email==email).first()

def get_users(db:Session,skip:int=0,limit:int=10):
   return db.query(model.User)\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_user(db:Session,user:schema.UserCreate):
  hahsed_password=pwd_context.hash(user.password)

  new_user=model.User(
    email=user.email,
    username=user.username,
    hashed_password=hahsed_password
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def create_post(db:Session,post:schema.PostCreate,user_id:int):
  new_post=model.Post(
    # post.dict() → converts Pydantic object to dictionary,** → unpacks fields like:
    **post.dict(),
    user_id=user_id
  )
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

def get_posts(db:Session,skip:int=0,limit:int=100):
  return db.query(model.Post)\
        .offset(skip)\
        .limit(limit)\
        .all()


