"""
File: whisper.py

Implements the WhisperAdapter using OpenAI's Whisper model.
Conforms to the TranscriberAdapter protocol.
"""
from typing import Optional
import whisper
from pipeline.utils.retry import retry
from pipeline.transcribers.adapters.base import TranscriberAdapter


class WhisperAdapter(TranscriberAdapter):
    """
    Transcribes audio using a locally loaded Whisper model.
    """
    def __init__(self, model_name: str = "base"):
        """
        Load the specified Whisper model variant.
        """
        self.model_name = model_name
        # type: ignore[attr-defined]
        self.model = whisper.load_model(model_name) # type: ignore[attr-defined]

    @retry(max_attempts=3)
    def transcribe(self, audio_path: str, language: Optional[str] = None) -> dict:
        """
        Run transcription on the given audio file.
        Returns a raw transcript dictionary.
        """
        return self.model.transcribe(audio_path, language = language)

    def get_engine_info(self) -> tuple[str, str]:
        """
        Return the engine name and model variant.
        """
        return ("whisper", self.model_name)
