from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User as UserModel
from schemas import UserCreate, User
from utils.security import get_password_hash
from services.auth import get_current_user
router = APIRouter()


@router.post("/", response_model=User)
def create_admin(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(username=user.username, password=hashed_password,
                        is_admin=True)  # Добавляем is_admin=True для администратора
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/ban/{user_id}")
def ban_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_admin:
        raise HTTPException(status_code=400, detail="Cannot ban/unban an admin user")

    user.is_active = False
    db.commit()
    return {"message": "User banned successfully"}


@router.put("/unban/{user_id}")
def unban_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()
    return {"message": "User unbanned successfully"}


@router.put("/promote/{user_id}")
def promote_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can promote users")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_admin = True
    db.commit()
    return {"message": "User promoted to admin successfully"}