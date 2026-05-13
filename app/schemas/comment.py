from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    text: str


class CommentOut(BaseModel):
    id: int
    text: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentList(BaseModel):
    comments: list[CommentOut]


CommentOut.model_rebuild()
CommentList.model_rebuild()
