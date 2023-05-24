import random
import string

from src.auth.service import UserService


def generate_random_string() -> str:

    letters = string.ascii_letters
    numbers = string.digits

    symbols = letters + numbers

    result_str = ''.join(random.choice(symbols) for _ in range(10))

    return result_str


def generate_random_slug() -> str:

    user_service = UserService.get_instance()
    slugs_db = user_service.get_all_slugs()

    while True:
        slug = generate_random_string()
        if slug not in slugs_db:
            break

    return slug