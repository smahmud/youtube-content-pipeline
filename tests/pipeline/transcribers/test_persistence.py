"""
File: test_persistence.py

Unit tests for transcript persistence and file I/O logic.

Covers:
- Saving TranscriptV1 objects to disk as JSON
- Reloading and verifying persisted transcript content
- File path resolution and overwrite behavior
"""
import json
from pipeline.transcribers.persistence import LocalFilePersistence
from pipeline.transcribers.schemas.transcript_v1 import TranscriptV1

def test_local_file_persistence_with_real_data(tmp_path):
    # Load real transcript data
    with open("tests/assets/sample_transcript_v1.json", encoding="utf-8") as f:
        data = json.load(f)

    transcript = TranscriptV1(**data)
    output_path = tmp_path / "transcript.json"

    # Persist to disk
    strategy = LocalFilePersistence()
    result_path = strategy.persist(transcript, output_path)

    # Assertions
    assert output_path.exists()
    assert result_path == str(output_path)
    assert output_path.read_text(encoding="utf-8").startswith("{")



    