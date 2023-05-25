from datetime import datetime, timedelta

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



