from dataclasses import dataclass
from uuid import UUID
import datetime


@dataclass
class AuthorDM:
    id: UUID
    name: str
    email: str
    created_at: datetime.datetime


@dataclass
class PostDM:
    id: UUID
    user_id: UUID
    text: str
    image_url: str | None
    created_at: datetime.datetime

    likes_count: int | None
    comments_count: int | None

    author: AuthorDM | None = None


@dataclass
class CommentDM:
    id: UUID
    post_id: UUID
    user_id: UUID
    text: str
    created_at: datetime.datetime


@dataclass
class LikeDM:
    id: UUID
    post_id: UUID
    user_id: UUID
    created_at: datetime.datetime
