from typing import List
from pydantic import BaseModel


class Segment(BaseModel):
    text: str
    start: float
    end: float


class Transcription(BaseModel):
    lang: str = "en"
    transcript : List[Segment] = []