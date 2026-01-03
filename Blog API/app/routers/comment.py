from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schema.comment import CommentCreate
from app.models.comment import Comment
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/posts/{post_id}/comments")
def add_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_comment = Comment(content=comment.content, post_id=post_id, user_id=user.id)
    db.add(new_comment)
    db.commit()
    return {"msg": "Comment added"}
