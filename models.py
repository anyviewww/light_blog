from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="articles")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    article_id = Column(Integer, ForeignKey("articles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")

User.articles = relationship("Article", order_by=Article.id, back_populates="author")
User.comments = relationship("Comment", order_by=Comment.id, back_populates="user")
Article.comments = relationship("Comment", order_by=Comment.id, back_populates="article")