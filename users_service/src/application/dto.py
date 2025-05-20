from dataclasses import dataclass
from uuid import UUID


@dataclass
class LoginUserDTO:
    email: str


@dataclass
class RegisterUserDTO:
    name: str
    email: str


@dataclass
class GetUsersByIdsDTO:
    user_ids: list[UUID]
