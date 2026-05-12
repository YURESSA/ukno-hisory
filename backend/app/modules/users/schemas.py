from pydantic import BaseModel, ConfigDict, EmailStr

from app.modules.users.models import UserRole


class UserCreate(BaseModel):
    email: EmailStr


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class AdminChangePasswordRequest(BaseModel):
    new_password: str


class ConfirmResetPassword(BaseModel):
    token: str
    new_password: str
