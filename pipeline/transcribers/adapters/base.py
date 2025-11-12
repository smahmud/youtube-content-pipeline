"""
File: base.py

Defines the TranscriberAdapter protocol for transcription adapters.
Used to enforce a consistent interface across adapter implementations.
"""
from typing import Protocol, Optional

class TranscriberAdapter(Protocol):
    """
    Protocol for transcription adapters.

    Implementations must provide:
    - Audio transcription from file path
    - Engine metadata reporting
    """
    def transcribe(self, audio_path: str, language: Optional[str] = None) -> dict:
        """
        ranscribe the given audio file and return a raw transcript dictionary.
        """

    def get_engine_info(self) -> tuple[str, str]:
        """
        Return the engine name and version used for transcription.
        """
