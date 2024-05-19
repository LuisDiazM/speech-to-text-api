import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from app.dependency_injector import get_faster_whisper_model
from infraestructure.transcriptor.faster_whisper import FasterWhisperTranscribe
from infraestructure.web.const import SUPPORT_TYPES
from infraestructure.web.middleware.auth import check_api_key
from infraestructure.web.schemas.transcribe_schema import Transcription


audios_to_process = APIRouter(tags=["Transcribe audios with faster whisper"], dependencies=[ Depends(check_api_key)])


@audios_to_process.post("/transcribe")
async def root(file: UploadFile, faster_whisper:FasterWhisperTranscribe = Depends(get_faster_whisper_model)) -> Transcription:
    try:
        file_type = file.content_type
        if file_type not in SUPPORT_TYPES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        file_bytes = await file.read()
        audio = io.BytesIO(file_bytes)
        transcribe = faster_whisper.transcribe(audio)
        return transcribe
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    