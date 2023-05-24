from typing import Union

from pydantic import BaseModel, EmailStr, root_validator


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str

    @root_validator
    def validate_password(cls, values):
        if not values.get("password") == values.get("password_confirm"):
            raise ValueError("Passwords don't match")
        values.pop("password_confirm")
        return values


class UserSchema(BaseModel):
    username: str
    email: str
    slug: str


class ActivateAccountSchema(BaseModel):
    activation_code: str


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: Union[str, None] = None