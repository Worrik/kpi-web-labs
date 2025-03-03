from abc import abstractmethod
from typing import Protocol

from src.domain.entities import UserDM


class UserRepo(Protocol):
    @abstractmethod
    async def create(self, name: str, email: str) -> UserDM: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDM | None: ...


class JWTTokenGenerator(Protocol):
    def generate_for_user(self, user: UserDM) -> str: ...


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...

    @abstractmethod
    async def execute(self, query) -> None: ...
