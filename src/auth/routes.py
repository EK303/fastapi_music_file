from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from jose import JWTError, jwt

from database import get_db, save
from src.config import settings
from .schemas import UserCreateSchema, ActivateAccountSchema, UserSchema, TokenData
from .models import User, create_new_user, get_user_by_username
from .authentication import oauth2_scheme, create_jwt_token, authenticate_user

auth_router = APIRouter()


@auth_router.post("/registration", status_code=status.HTTP_201_CREATED,
                  tags=["users"])
async def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):

    if db.query(User).filter_by(email=user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")

    await create_new_user(user, db=db)

    return {"username": user.username,
            "email": user.email}


@auth_router.post("/activate",
                  status_code=status.HTTP_200_OK,
                  tags=["users"])
async def activate_account(code: ActivateAccountSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.activation_code == code.activation_code).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid activation code")

    if not user.is_active:
        user.activation_code = ""
        user.is_active = True
        await save(user, db)

        return {"message": "Your account has been activated"}

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is already active")


@auth_router.post("/login",
                  status_code=status.HTTP_200_OK,
                  tags=["users"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Failed to login. Possible reasons:"
                                                                          "1: Account is not activated;"
                                                                          "2: Incorrect email or password")

    jwt_token = create_jwt_token(user["username"])

    if jwt_token:
        return {"access_token": jwt_token, "token_type": "bearer"}

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Couldn't generate token")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


@auth_router.get("/profile",
                 status_code=status.HTTP_200_OK,
                 response_model=UserSchema)
async def profile(current_user: User = Depends(get_current_user)):
    data = {
        "username": current_user.username,
        "email": current_user.email
    }
    return UserSchema(**data)
