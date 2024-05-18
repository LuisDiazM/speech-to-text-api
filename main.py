from faster_whisper import WhisperModel
from fastapi import FastAPI, UploadFile, HTTPException, status, Depends
from auth import check_api_key
from const import SUPPORT_TYPES
from transcribe_model import Transcription, Segment
import io
import os
import sys

model_faster_whisper = os.getenv("MODEL_PATH")
if model_faster_whisper == "":
    sys.exit(0)

model = WhisperModel(model_faster_whisper, device="cpu", compute_type="int8")

app = FastAPI()

@app.post("/transcribe")
async def root(file: UploadFile, valid:bool = Depends(check_api_key)) -> Transcription:
    file_type = file.content_type
    if file_type not in SUPPORT_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    file_bytes = await file.read()
    audio = io.BytesIO(file_bytes)
    segments, info = model.transcribe(audio, beam_size=5)
    transcription_segments = []
    for segment in segments:
        segment_data = Segment(text=segment.text, start=segment.start, end=segment.end)
        transcription_segments.append(segment_data)
    return Transcription(lang=info.language, transcript=transcription_segments)


