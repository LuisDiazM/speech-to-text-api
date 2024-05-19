

## infraestructure
from infraestructure.transcriptor.faster_whisper import FasterWhisperTranscribe


async def get_faster_whisper_model()-> FasterWhisperTranscribe:
    return FasterWhisperTranscribe()