from typing import Union

from pydantic import BaseModel


class AudioFileSchema(BaseModel):

    link: Union[str, None] = None
