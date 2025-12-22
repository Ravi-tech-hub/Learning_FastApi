from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
  __tablename__="users"
  id=Column(Integer,primary_key=True,index=True)
  email=Column(String,unique=True,index=True,nullable=False)
  username=Column(String,unique=True,index=True,nullable=False)
  hashed_password=Column(String,nullable=False)
  is_active = Column(Boolean, default=True)
  created_at=Column(DateTime(timezone=True),server_default=func.now())
  posts=relationship("Post",back_populates="author")

class Post(Base):
  __tablename__="posts"
  id=Column(Integer,primary_key=True,index=True)
  title=Column(String,index=True,nullable=False)
  content=Column(String,nullable=False)
  user_id=Column(Integer,ForeignKey("users.id"))
  created_at=Column(DateTime(timezone=True),server_default=func.now())
  author=relationship("User",back_populates="posts")



