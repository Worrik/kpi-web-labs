from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.entities import CommentDM, LikeDM, PostDM


class PostRepo(Protocol):
    @abstractmethod
    async def create_post(
        self,
        user_id: UUID,
        text: str,
        image_url: str | None,
    ) -> PostDM: ...

    @abstractmethod
    async def get_posts(self) -> list[PostDM]: ...

    @abstractmethod
    async def get_post_by_id(self, post_id: UUID) -> PostDM: ...

    @abstractmethod
    async def update_post_image(
        self,
        post_id: UUID,
        image_url: str,
    ) -> PostDM: ...


class CommentRepo(Protocol):
    @abstractmethod
    async def create_comment(self, post_id: UUID, user_id: UUID, text: str) -> CommentDM: ...

    @abstractmethod
    async def get_comments(self, post_id: UUID) -> list[CommentDM]: ...


class LikeRepo(Protocol):
    @abstractmethod
    async def create_like(self, post_id: UUID, user_id: UUID) -> LikeDM: ...


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...

    @abstractmethod
    async def execute(self, query) -> None: ...
