"""
File: test_validate.py

Unit tests for schema validation logic applied to raw transcript dictionaries.

Covers:
- Validation of raw transcript dicts against TranscriptV1 schema
- Detection of malformed or incomplete transcript structures
- Return of validated TranscriptV1 objects from dict input
"""
from datetime import datetime
import pytest
from pipeline.transcribers.validate import validate_transcript_v1, TranscriptValidationError
from pipeline.transcribers.schemas.transcript_v1 import TranscriptV1

@pytest.fixture
def valid_transcript_dict():
    return {
        "metadata": {
            "engine": "whisper",
            "engine_version": "base",
            "language": "en",
            "confidence_avg": 0.92,
            "schema_version": "v1",
            "created_at": datetime.utcnow().isoformat(timespec="milliseconds")
        },
        "transcript": [
            {"text": "Hello world", "timestamp": "00:00:00.000", "confidence": 0.95},
            {"text": "This is a test", "timestamp": "00:00:02.500", "confidence": 0.89}
        ]
    }

@pytest.fixture
def invalid_transcript_dict():
    return {
        "metadata": {
            "engine": "whisper",
            "engine_version": "base",
            "language": "en",
            "confidence_avg": "high"  #  should be float
        },
        "transcript": [
            {"text": "Oops", "timestamp": "not-a-timestamp", "confidence": "sure"}  #  multiple type errors
        ]
    }

def test_validate_transcript_success(valid_transcript_dict):
    result = validate_transcript_v1(valid_transcript_dict)
    assert isinstance(result, TranscriptV1)
    assert result.metadata.language == "en"
    assert len(result.transcript) == 2

def test_validate_transcript_failure(invalid_transcript_dict):
    with pytest.raises(TranscriptValidationError) as exc_info:
        validate_transcript_v1(invalid_transcript_dict)

    err = exc_info.value
    assert isinstance(err, TranscriptValidationError)
    assert isinstance(err.errors, list)
    assert any("confidence_avg" in str(e["loc"]) for e in err.errors)
    assert any("timestamp" in str(e["loc"]) for e in err.errors)

def test_validate_transcript_with_extra_fields(valid_transcript_dict):
    data = valid_transcript_dict.copy()
    data["unexpected"] = "value"

    with pytest.raises(TranscriptValidationError) as exc_info:
        validate_transcript_v1(data)

    assert "Extra inputs are not permitted" in str(exc_info.value.errors)

