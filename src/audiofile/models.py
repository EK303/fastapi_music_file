import uuid

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from .service import Result

Base = declarative_base()


class AudioFile(Base):
    __tablename__ = "audiofile"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, nullable=False)
    link = Column(String, unique=True, nullable=True)
    path_to_file = Column(String, unique=True, nullable=False)
    uploader_slug = Column(String, nullable=False)


def create_audio_file(user, file_path, db: Session):
    try:
        uuid_number = uuid.uuid4()
        download_url = f"id={uuid_number}&user={user.slug}"

        file = AudioFile(uuid=uuid_number,
                         link=download_url,
                         path_to_file=file_path,
                         uploader_slug=user.slug)

        db.add(file)
        db.commit()
        db.refresh(file)

        return Result.success(status=True, url=download_url, file_path=file_path,
                              uuid_number=uuid_number)

    except IntegrityError:
        return Result.fail(status=False, message="A file with this name already exists")
