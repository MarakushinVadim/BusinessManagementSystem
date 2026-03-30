from fastapi import APIRouter
from starlette import status

router = APIRouter(prefix="users", tags=["users"])

# @router.post('/register', status_code=status.HTTP_201_CREATED)
