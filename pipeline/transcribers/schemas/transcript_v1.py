"""
File: transcript_v1.py

Defines the TranscriptV1 schema used for normalized transcript output.
Includes segment structure, metadata model, and metadata construction utility.
"""
from datetime import datetime, UTC
from typing import List, Optional
from pydantic import BaseModel, field_validator, Field, ValidationInfo, ConfigDict

class TranscriptSegment(BaseModel):
    """
    A single segment of transcribed text with optional speaker and confidence.
    """
    text: str
    timestamp: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, v: str, info: ValidationInfo) -> str:
        try:
            datetime.strptime(v, "%H:%M:%S.%f")
        except ValueError:
            raise ValueError("Timestamp must be in HH:MM:SS.mmm format")
        return v

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: Optional[float], info: ValidationInfo) -> Optional[float]:
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class TranscriptMetadata(BaseModel):
    """
    Metadata describing the transcript source, schema, language, and engine details.
    """
    engine: str
    engine_version: str
    schema_version: str
    created_at: datetime
    language: Optional[str] = None
    confidence_avg: Optional[float] = None


class TranscriptV1(BaseModel):
    """
    Normalized transcript format used across the pipeline.
    Includes metadata, full text, and structured segments.
    """
    metadata: TranscriptMetadata
    transcript: List[TranscriptSegment] = Field(default_factory=list)
    model_config = ConfigDict(extra="forbid")  # Pydantic v2

def build_transcript_metadata(
    engine: str,
    engine_version: str,
    schema_version: str = "transcript_v1",
    language: Optional[str] = None,
    confidence_avg: Optional[float] = None,
) -> TranscriptMetadata:
    """
    Construct transcript metadata from engine details and optional parameters.
    Sets the creation timestamp and schema version.

    Returns:
        TranscriptMetadata: Populated metadata object.
    """    
    return TranscriptMetadata(
        engine=engine,
        engine_version=engine_version,
        schema_version=schema_version,
        created_at=datetime.now(UTC),
        language=language,
        confidence_avg=confidence_avg,
    )
