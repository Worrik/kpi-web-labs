from pydantic import BaseModel, EmailStr


class LoginUserSchema(BaseModel):
    email: EmailStr


class RegisterUserSchema(BaseModel):
    name: str
    email: EmailStr
