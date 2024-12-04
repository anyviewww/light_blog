from fastapi import FastAPI
from database import engine, Base
from routers import users, articles, comments, auth

app = FastAPI()

#Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(articles.router, prefix="/articles", tags=["articles"])
app.include_router(comments.router, prefix="/articles", tags=["comments"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)