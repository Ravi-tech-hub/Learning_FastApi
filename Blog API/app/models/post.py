from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base

class Post(Base):
  __tablename__="posts"
  id=Column(Integer, primary_key=True, index=True)
  title=Column(String(255), nullable=False)
  content=Column(Text, nullable=False)
  image_url=Column(String,nullable=True)

  author_id=Column(Integer,ForeignKey("users.id"))
  category_id=Column(Integer,ForeignKey("categories.id"))

  author=relationship("User")
  category=relationship("Category")
  