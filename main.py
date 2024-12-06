import logging
from fastapi import FastAPI
from database import engine, Base
import threading
import uvicorn
from routers import users, articles, comments, auth, admin
from fastapi import Request
from fastapi.responses import JSONResponse
from services.bot import send_telegram_message, start_bot


logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
#app = FastAPI()
app = FastAPI(
    title="Light Blog API",
    description="API documentation for Light Blog",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

#Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(articles.router, prefix="/articles", tags=["articles"])
app.include_router(comments.router, prefix="/articles", tags=["comments"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    logger.error(f"Internal Server Error: {exc}")
    send_telegram_message(f"Internal Server Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

@app.get("/")
async def read_root():
    return {"Welcome to the application!"}

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_flask():
    start_bot()

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi)
    flask_thread = threading.Thread(target=run_flask)

    fastapi_thread.start()
    flask_thread.start()

    fastapi_thread.join()
    flask_thread.join()