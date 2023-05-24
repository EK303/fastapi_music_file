import os
from pathlib import Path
from decouple import config
import string


class Settings:
    # database settings
    SQLALCHEMY_DATABASE_URL = f"{config('DB_ENGINE')}://{config('DB_USER')}:" \
                              f"{config('DB_PASSWORD')}@{config('DB_HOST')}/{config('DB_NAME')}"

    # mailing settings
    MAIL_USERNAME = config("MAIL_USERNAME")
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    MAIL_FROM = config('MAIL_FROM')
    MAIL_PORT = int(config('MAIL_PORT'))
    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_FROM_NAME = config('MAIN_FROM_NAME')

    alphabet = string.ascii_letters + string.digits + '!#$%&()*+,-.:;<=>?@[]^_`{|}~'

    # authentication
    PWD_ALGORITHM = config("PWD_ALGORITHM")
    JWT_SECRET = config("JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))
    JWT_ALGORITHM = config("JWT_ALGORITHM")

    root_directory = Path.cwd()
    files_directory = os.path.join(root_directory, 'static')


settings = Settings()
