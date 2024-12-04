from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User as UserModel
from schemas import UserCreate, User
from utils.security import get_password_hash

router = APIRouter()

@router.post("/", response_model=User)
def create_admin(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(username=user.username, password=hashed_password, is_admin=True)  # Добавляем is_admin=True для администратора
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
