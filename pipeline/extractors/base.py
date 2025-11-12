"""
File: base.py

Defines the extractor interface for audio and metadata operations in the content-pipeline project.
"""
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """
    Abstract interface for platform-specific extractors.
    """
    @abstractmethod
    def extract_audio(self, source: str, output_path: str) -> str:
        """
        Abstract method for extracting audio from a media source.

        Must be implemented by subclasses to handle specific input formats and extraction logic.
        """
        pass

    @abstractmethod
    def extract_metadata(self, source: str) -> dict:
        """
        Abstract method for extracting metadata from a media source.

        Must be implemented by subclasses to return structured metadata for downstream enrichment.
        """
        pass

