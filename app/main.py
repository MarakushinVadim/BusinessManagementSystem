from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from redis import asyncio as aioredis
from fastapi import FastAPI
from sqladmin import Admin

from app.auth.auth import admin_authentication_backend
from app.auth.auth_routers import auth_router
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware

from app import routers
from app.database import engine
from app.config import SECRET_KEY
from app.models import UserAdminView, TaskAdminView

logger.add("info.log")

SECRET = SECRET_KEY


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    pool = aioredis.ConnectionPool.from_url("redis://localhost", decode_responses=True)
    app.state.redis = aioredis.Redis(connection_pool=pool)

    yield

    await app.state.redis.close()
    await pool.disconnect()


app = FastAPI(lifespan=lifespan, title="Business Management System")


app.add_middleware(SessionMiddleware, secret_key=SECRET)

admin = Admin(
    app=app, engine=engine, authentication_backend=admin_authentication_backend
)

admin.add_view(UserAdminView)
admin.add_view(TaskAdminView)

app.include_router(auth_router)
app.include_router(routers.task_router)


@app.get("/")
async def get_main():
    return {"message": "hello"}
