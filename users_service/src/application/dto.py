from dataclasses import dataclass


@dataclass
class LoginUserDTO:
    email: str


@dataclass
class RegisterUserDTO:
    name: str
    email: str
