import secrets
from passlib.context import CryptContext

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from src.config import settings


secure_random = secrets.SystemRandom()


def generate_activate_code():
    random_string = "".join(secure_random.choice(settings.alphabet) for _ in range(20))

    return random_string


pwd_context = CryptContext(schemes=[settings.PWD_ALGORITHM], deprecated="auto")


class Hasher:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_mail(user_email, activation_code):

    fm = FastMail(conf)
    message = MessageSchema(
        subject="Activation Code",
        recipients=[user_email, ],
        body=f"Activate your account {str(activation_code)}",
        subtype="plain"
    )

    await fm.send_message(message)


