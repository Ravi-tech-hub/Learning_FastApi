from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schema.post import PostCreate, PostResponse
from app.models.post import Post
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_post = Post(**post.dict(), author_id=user.id)
    db.add(new_post)
    db.commit()
    return new_post

@router.get("/")
def list_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()
