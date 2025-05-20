from pydantic import BaseModel
from uuid import UUID

import datetime


class AuthorSchema(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime.datetime


class PostSchema(BaseModel):
    id: UUID
    created_at: datetime.datetime
    user_id: UUID
    text: str
    image_url: str | None
    likes_count: int | None
    comments_count: int | None
    author: AuthorSchema | None = None

class CreatePostSchema(BaseModel):
    text: str
    image_data: str | None = None


class CreateCommentSchema(BaseModel):
    text: str


class CommentSchema(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    text: str
    created_at: datetime.datetime
    author: AuthorSchema | None = None
