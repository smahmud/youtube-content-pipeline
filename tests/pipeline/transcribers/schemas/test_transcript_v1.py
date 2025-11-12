"""
File: test_transcript_v1.py

Unit tests for TranscriptV1 schema models and utilities.

Covers:
- Construction and validation of TranscriptSegment and TranscriptMetadata
- Metadata generation via build_transcript_metadata
- Pydantic model behavior and serialization
"""
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from pipeline.transcribers.schemas.transcript_v1 import TranscriptV1, TranscriptSegment, TranscriptMetadata, build_transcript_metadata 

@pytest.fixture
def valid_segment():
    return TranscriptSegment(
        text="Hello world",
        timestamp="00:00:01.000",
        speaker="Speaker 1",
        confidence=0.95
    )


@pytest.fixture
def valid_metadata():
    return TranscriptMetadata(
        engine="whisper",
        engine_version="1.0.0",
        schema_version="transcript.v1",
        created_at=datetime.now(timezone.utc),
        language="en",
        confidence_avg=0.95
    )


def test_valid_transcript(valid_segment, valid_metadata):
    transcript = TranscriptV1(
        metadata=valid_metadata,
        transcript=[valid_segment]
    )
    assert transcript.metadata.engine == "whisper"
    assert transcript.transcript[0].text == "Hello world"


def test_invalid_timestamp():
    with pytest.raises(ValueError) as exc_info:
        TranscriptSegment(
            text="Bad timestamp",
            timestamp="not-a-time",
            confidence=0.9
        )
    assert "Timestamp must be in HH:MM:SS.mmm format" in str(exc_info.value)


def test_invalid_confidence():
    with pytest.raises(ValueError) as exc_info:
        TranscriptSegment(
            text="Bad confidence",
            timestamp="00:00:01.000",
            confidence=1.5
        )
    assert "Confidence must be between 0.0 and 1.0" in str(exc_info.value)


def test_missing_text():
    with pytest.raises(ValidationError) as exc_info:
        TranscriptSegment(
            timestamp="00:00:01.000",
            confidence=0.9
        )
    assert "Field required" in str(exc_info.value)
    assert "text" in str(exc_info.value)


def test_build_transcript_metadata():
    metadata = build_transcript_metadata(
        engine="whisper",
        engine_version="1.0.0",
        language="en",
        confidence_avg=0.85
    )

    assert isinstance(metadata, TranscriptMetadata)
    assert metadata.engine == "whisper"
    assert metadata.engine_version == "1.0.0"
    assert metadata.schema_version == "transcript_v1"
    assert metadata.language == "en"
    assert metadata.confidence_avg == 0.85
    assert metadata.created_at is not None

def test_build_transcript_metadata_missing_optional_fields():
    metadata = build_transcript_metadata(engine="whisper", engine_version="base")
    assert metadata.language is None
    assert metadata.confidence_avg is None

def test_build_transcript_metadata_created_at_format():
    metadata = build_transcript_metadata(engine="whisper", engine_version="base")
    dt = metadata.created_at
    assert dt.tzinfo is not None
    assert dt.isoformat().endswith("Z") or "+00:00" in dt.isoformat()
