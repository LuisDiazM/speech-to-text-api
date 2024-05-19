from io import BytesIO
from faster_whisper import WhisperModel
import os
import sys

from app.singleton import SingletonMeta
from infraestructure.transcriptor.entities import Segment, Transcription
from app.logging import logger_app
class FasterWhisperTranscribe(metaclass=SingletonMeta):
    def __init__(self) -> None:
        model_faster_whisper = os.getenv("MODEL_PATH")
        device = os.getenv("DEVICE")
        precision = os.getenv("PRECISION_DEVICE")
        if model_faster_whisper == "" or device == "" or precision == "":
            sys.exit(0)
        self.model = WhisperModel(model_faster_whisper, device=device, compute_type=precision)
        logger_app.info("faster whisper model loaded!!!")
    

    def transcribe(self, audio: BytesIO)-> Transcription:
        segments, info = self.model.transcribe(audio, beam_size=5)
        transcription_segments = []
        for segment in segments:
            segment_data = Segment(text=segment.text, start=segment.start, end=segment.end)
            transcription_segments.append(segment_data)
        return Transcription(lang=info.language, transcript=transcription_segments)
