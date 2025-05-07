import datetime
from uuid import UUID
from pydantic import BaseModel


class CreatePostSchema(BaseModel):
    user_id: UUID
    text: str
    image_data: str | None = None


class CreateLikeSchema(BaseModel):
    post_id: UUID
    user_id: UUID


class CreateCommentSchema(BaseModel):
    post_id: UUID
    user_id: UUID
    text: str


class PostSchema(BaseModel):
    id: UUID
    user_id: UUID
    text: str
    created_at: datetime.datetime
    image_url: str | None = None
    likes_count: int | None = None
    comments_count: int | None = None


class ChangeImageSchema(BaseModel):
    post_id: UUID
    user_id: UUID
    image_url: str
