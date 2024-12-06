from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Comment, User
from schemas import CommentCreate, Comment
from services.auth import get_current_user


router = APIRouter()

@router.post("/{article_id}/comments/", response_model=Comment)
def create_comment(article_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_comment = Comment(**comment.dict(), article_id=article_id, user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/{article_id}/comments/{comment_id}", response_model=Comment)
def delete_comment(article_id: int, comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(db_comment)
    db.commit()
    return db_comment