from fastapi import FastAPI
from app.auth.auth_routers import auth_router
from loguru import logger

logger.add("info.log")

app = FastAPI(title="Business Management System")

app.include_router(auth_router)


@app.get("/")
async def get_main():
    return {"message": "hello"}
