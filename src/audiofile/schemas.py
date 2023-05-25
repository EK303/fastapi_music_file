from typing import Union

from pydantic import BaseModel


class AudioFileSchema(BaseModel):

    link: Union[str, None] = None


class AudioFilePathSchema(BaseModel):

    uuid_number: Union[str, None] = None
    link: Union[str, None] = None
    path: Union[str, None] = None
    uploader_slug: Union[str, None] = None

