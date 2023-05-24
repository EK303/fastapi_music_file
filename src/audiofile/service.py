class Result:

    def __init__(self, *args, **kwargs):
        self.status = kwargs.get("status", None)
        self.message = kwargs.get("message", None)
        self.file_path = kwargs.get("file_path", None)

    @classmethod
    def success(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @classmethod
    def fail(cls, *args, **kwargs):
        return cls(*args, **kwargs)


class OperationalError(BaseException):
    pass
