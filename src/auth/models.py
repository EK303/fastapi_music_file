from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from .schemas import UserCreateSchema
from .utils import Hasher, generate_activate_code, send_mail
from src.slugging import generate_random_slug


Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    activation_code = Column(String)
    is_active = Column(Boolean, default=False)
    slug = Column(String, unique=True, nullable=True)


async def create_new_user(user: UserCreateSchema, db: Session):

    slug = generate_random_slug()

    user = User(username=user.username,
                email=user.email,
                password=Hasher.hash_password(user.password),
                activation_code=generate_activate_code(),
                is_active=False,
                slug=slug)
    db.add(user)
    db.commit()
    db.refresh(user)

    # send activation code
    await send_mail(user.email, user.activation_code)
    return user


def get_user_by_username(username: str, db):
    user = db.query(User).filter_by(username=username).first()
    return user
