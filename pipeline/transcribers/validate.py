"""
File: validate.py

Provides validation utilities for checking TranscriptV1 schema compliance.
Raises TranscriptValidationError on failure.
"""
from typing import Any
from pydantic import ValidationError
from pipeline.transcribers.schemas.transcript_v1 import TranscriptV1

class TranscriptValidationError(Exception):
    """
    Raised when transcript validation fails.
    Includes optional structured error details.
    """
    def __init__(self, message: str, errors: Any = None):
        """
        Initialize the exception with a message and optional error details.
        """
        super().__init__(message)
        self.errors = errors

def validate_transcript_v1(data: dict) -> TranscriptV1:
    """
    Validate a dictionary against the TranscriptV1 schema.
    Returns a parsed TranscriptV1 object or raises TranscriptValidationError.
    """
    try:
        return TranscriptV1(**data)
    except ValidationError as e:
        raise TranscriptValidationError("Transcript validation failed", errors=e.errors())
