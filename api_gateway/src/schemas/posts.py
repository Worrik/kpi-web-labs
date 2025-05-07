from pydantic import BaseModel
from uuid import UUID

import datetime


class PostSchema(BaseModel):
    id: UUID
    created_at: datetime.datetime
    user_id: UUID
    text: str
    image_url: str | None
    likes_count: int | None
    comments_count: int | None


class CreatePostSchema(BaseModel):
    text: str
    image_url: str | None


class CreateCommentSchema(BaseModel):
    text: str
