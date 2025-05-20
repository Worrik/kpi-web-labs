from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.entities import UserDM


class UserRepo(Protocol):
    @abstractmethod
    async def create(
        self,
        name: str,
        email: str,
    ) -> UserDM: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDM | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserDM | None: ...

    @abstractmethod
    async def get_by_ids(self, user_ids: list[UUID]) -> list[UserDM]: ...


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...

    @abstractmethod
    async def execute(self, query) -> None: ...
