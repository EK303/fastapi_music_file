from fastapi import FastAPI

from src.auth.routes import auth_router
from src.audiofile.routes import file_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(file_router)