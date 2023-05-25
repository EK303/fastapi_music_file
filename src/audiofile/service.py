from sqlalchemy.sql import text

from database import get_db

db = next(get_db())


# to keep track of statuses and descriptions of tasks performed by the application and catch
# errors that may occur to see their nature
class Result:

    def __init__(self, *args, **kwargs):
        self.status = kwargs.get("status", None)
        self.message = kwargs.get("message", None)
        self.file_path = kwargs.get("file_path", None)
        self.url = kwargs.get("url", None)
        self.uuid_number = kwargs.get("uuid_number", None)

    @classmethod
    def success(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @classmethod
    def fail(cls, *args, **kwargs):
        return cls(*args, **kwargs)


# to avoid requests to the database, we set a class with a single instance
# possible that will store all the necessary information we might need
class FileService:
    paths: set = {}
    urls: set = {}
    uuids: set = {}
    urls_path: list = []
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._get_all_urls()
        return cls._instance

    def _get_all_urls(self):

        if not self.urls:
            query = text("SELECT * FROM audiofile;")
            connection = db.execute(query)
            result = connection.fetchall()
            self.uuids = set([item[1] for item in result])
            self.urls = set([item[2] for item in result])
            self.paths = set([item[3] for item in result])
            self.urls_path = [{"uuid_number": item[1], "link": item[2], "path": item[3], "uploader_slug": item[4]}
                              for item in result]
        return self.urls_path

    def get_all_urls(self):
        return self.urls

    def get_all_urls_path(self):
        return self.urls_path

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def update_url(self, url: str):
        self.urls.add(url)

    def update_url_path(self, url: str, file_path: str, uuid_number: str):
        if file_path not in self.paths:
            self.urls_path.append({"uuid_number": uuid_number, "link": url, "path": file_path})
            self.paths.add(file_path)
            self.urls.add(url)

    def download_file(self, uuid_number: str):

        if not uuid_number in self.uuids:
            return Result.fail(status=False, message="File not found")

        for file in self.urls_path:
            if file["uuid_number"] == uuid_number:
                return Result.success(status=True, file_path=file["path"])
