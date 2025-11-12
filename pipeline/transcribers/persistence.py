"""
File: persistence.py

Defines persistence strategies for saving transcript objects to local or remote destinations.
Includes protocol interfaces and concrete implementations.
"""
from typing import Protocol, Union
from pathlib import Path

class SerializableTranscript(Protocol):
    """
    Interface for transcript objects that can be serialized to a dictionary.
    """
    def model_dump(self) -> dict:
        ...

class TranscriptPersistenceStrategy(Protocol):
    """
    Interface for persistence strategies that store transcript objects to a destination.
    """
    def persist(self, transcript: SerializableTranscript, destination: Union[str, Path]) -> str:
        ...

class LocalFilePersistence:
    """
    Persists a transcript object to a local JSON file.
    """
    def persist(self, transcript: SerializableTranscript, destination: Union[str, Path]) -> str:
        """
        Write the transcript to a local file as formatted JSON.
        Returns the path to the saved file.
        """
        path = Path(destination)
        with open(path, "w") as f:
            f.write(transcript.model_dump_json(indent=2))
        return str(path)

class CloudPersistence:
    """
    Stub implementation for uploading transcripts to a cloud destination.
    """
    def persist(self, transcript: SerializableTranscript, destination: str) -> str:
        # Upload to cloud
        return destination  # e.g., S3 URL
