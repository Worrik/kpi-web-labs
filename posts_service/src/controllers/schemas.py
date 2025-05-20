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


class AuthorSchema(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime.datetime


class PostSchema(BaseModel):
    id: UUID
    user_id: UUID
    text: str
    created_at: datetime.datetime
    image_url: str | None = None
    likes_count: int | None = None
    comments_count: int | None = None
    author: AuthorSchema | None = None


class ChangeImageSchema(BaseModel):
    post_id: UUID
    user_id: UUID
    image_url: str


class CommentSchema(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    text: str
    created_at: datetime.datetime
    author: AuthorSchema | None = None
