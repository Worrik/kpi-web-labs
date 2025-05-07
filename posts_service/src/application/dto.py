from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreatePostDTO:
    user_id: UUID
    text: str
    image_data: str | None = None


@dataclass
class CreateLikeDTO:
    post_id: UUID
    user_id: UUID


@dataclass
class CreateCommentDTO:
    post_id: UUID
    user_id: UUID
    text: str


@dataclass
class ChangeImageDTO:
    user_id: UUID
    post_id: UUID
    image_url: str
