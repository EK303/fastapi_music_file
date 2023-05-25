from sqlalchemy.sql import text

from database import get_db

db = next(get_db())


# to avoid requests to the database, we set a class with a single instance
# possible that will store all the necessary information we might need
class UserService:
    slugs = {}
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._get_all_slugs()
        return cls._instance

    def _get_all_slugs(self):
        if not self.slugs:
            query = text("SELECT * FROM users;")
            connection = db.execute(query)
            result = connection.fetchall()
            self.slugs = set([item["slug"] for item in result])

    def get_all_slugs(self):
        return self.slugs

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
