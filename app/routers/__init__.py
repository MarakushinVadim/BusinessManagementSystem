from .task import router as task_router
from .comment import router as comment_router
from .meetings import router as meeting_router
from .users import router as users_router
from .calendar import router as calendar_router

__all__ = [
    "task_router",
    "comment_router",
    "meeting_router",
    "users_router",
    "calendar_router",
]
