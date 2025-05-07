from pydantic import BaseModel, EmailStr


class LoginUserSchema(BaseModel):
    email: EmailStr


class RegisterUserSchema(BaseModel):
    name: str
    email: EmailStr


class AccessTokenResponse(BaseModel):
    access_token: str
