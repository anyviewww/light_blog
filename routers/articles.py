from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Article, User
from schemas import ArticleCreate, Article
from typing import List
from services.auth import get_current_user  # Импортируйте функцию get_current_user

router = APIRouter()

@router.post("/", response_model=Article, summary="Create a new article", description="Create a new article with the provided title and content.")
def create_article(article: ArticleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_article = Article(**article.dict(), author_id=current_user.id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.get("/", response_model=List[Article], summary="Get a list of articles", description="Retrieve a list of all articles.")
def get_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

@router.get("/{article_id}", response_model=Article, summary="Get an article by ID", description="Retrieve an article by its ID.")
def get_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.delete("/{article_id}", response_model=Article, summary="Delete an article by ID", description="Delete an article by its ID.")
def delete_article(article_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if db_article.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(db_article)
    db.commit()
    return db_article



"""
router = APIRouter()

@router.post("/", response_model=Article)
def create_article(article: ArticleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_article = Article(**article.dict(), author_id=current_user.id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.get("/", response_model=List[Article])
def get_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

@router.get("/{article_id}", response_model=Article)
def get_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.delete("/{article_id}", response_model=Article)
def delete_article(article_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if db_article.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(db_article)
    db.commit()
    return db_article

"""