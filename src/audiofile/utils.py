import os
from pydub import AudioSegment

from src.config import settings

from .service import Result, OperationalError


def check_file_format(file):

    if file.filename.endswith('.wav'):
        return Result.success(status=True)

    return Result.fail(status=False, message="File format not supported")


async def convert_save_wav_to_mp3(file):
    os.makedirs(settings.files_directory, exist_ok=True)

    try:
        wav_file_path = os.path.join(settings.files_directory, file.filename)
        with open(wav_file_path, 'wb') as wav_file:
            wav_file.write(await file.read())

        audio = AudioSegment.from_file(wav_file_path, format="wav")

        mp3_file = file.filename.replace('.wav', '.mp3')
        mp3_file_path = os.path.join(settings.files_directory, mp3_file)
        audio.export(mp3_file_path, format="mp3")

        os.remove(wav_file_path)

        return Result.success(status=True, file_path=mp3_file_path)

    except OperationalError as e:
        return Result.fail(status=False, message=str(e))
