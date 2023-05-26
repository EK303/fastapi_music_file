from datetime import datetime, timedelta

from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from .models import get_user_by_username
from .utils import Hasher
from src.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(username: str, password: str, db):
    user = get_user_by_username(username, db)

    if not user.is_active:
        return None
    if not user or not Hasher.verify_password(password, user.password):
        return None

    return {
        "username": user.username,
    }


def create_jwt_token(username: str):
    try:
        expiration_time = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        jwt_payload = {"sub": username, "exp": expiration_time}
        jwt_token = jwt.encode(jwt_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return jwt_token

    except JWTError:
        return None


def token_error(error_message: str):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=error_message,
                        headers={"WWW-Authenticate": "Bearer"})


