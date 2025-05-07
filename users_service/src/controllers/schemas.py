import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr


class LoginUserSchema(BaseModel):
    email: EmailStr


class RegisterUserSchema(BaseModel):
    name: str
    email: EmailStr


class UserSchema(BaseModel):
    id: UUID
    created_at: datetime.datetime
    name: str
    email: EmailStr


class ErrorResponse(BaseModel):
    detail: str
