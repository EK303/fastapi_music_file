from typing import Annotated, List

from fastapi import UploadFile, APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.routes import get_current_user

from database import get_db

from .models import create_audio_file
from .schemas import AudioFileSchema, AudioFilePathSchema
from .service import FileService
from .utils import check_file_format, convert_save_wav_to_mp3

file_router = APIRouter()

file_service = FileService.get_instance()


@file_router.post("/upload",
                  response_model=AudioFileSchema,
                  status_code=status.HTTP_201_CREATED,
                  tags=["audio"])
async def upload_file(file: UploadFile,
                      current_user: Annotated[User, Depends(get_current_user)],
                      db: Session = Depends(get_db)):

    check_file = check_file_format(file)

    if not check_file.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=check_file.message)

    process_file = await convert_save_wav_to_mp3(file)

    if not process_file.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=process_file.message)

    save_file = create_audio_file(user=current_user, file_path=process_file.file_path, db=db)

    if not save_file.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=save_file.message)

    file_service.update_url_path(save_file.url, save_file.file_path)

    return {"link": save_file.url}


@file_router.get("/list",
                 response_model=List[AudioFilePathSchema],
                 status_code=status.HTTP_200_OK,
                 tags=["audio"])
async def get_list_urls():

    list_files = file_service.get_all_urls_path()

    return list_files
