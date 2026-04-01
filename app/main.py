from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from app.auth.auth_routers import auth_router
from loguru import logger

# from examples.models import Admin

logger.add("info.log")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    pool = aioredis.ConnectionPool.from_url("redis://localhost", decode_responses=True)
    redis_client = aioredis.Redis(connection_pool=pool)

    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=["templates"],
        providers=[
            UsernamePasswordProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ],
        redis=redis_client,
    )
    yield
    await redis_client.close()
    await pool.disconnect()


app = FastAPI(lifespan=lifespan, title="Business Management System")
app.mount("/admin", admin_app)
app.include_router(auth_router)


@app.get("/")
async def get_main():
    return {"message": "hello"}
