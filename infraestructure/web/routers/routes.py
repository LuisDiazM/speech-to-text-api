from fastapi import APIRouter
from infraestructure.web.routers.transcribe import audios_to_process

routers = APIRouter()
routers.include_router(audios_to_process)