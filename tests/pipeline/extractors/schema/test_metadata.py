"""
File: test_metadata.py

Unit tests for metadata schema constructors.

Covers:
- build_local_placeholder_metadata() structure and defaults
- build_base_metadata() behavior via indirect validation
"""
from pipeline.extractors.schema.metadata import build_local_placeholder_metadata

def test_build_local_placeholder_metadata_returns_expected_structure(tmp_path):
    dummy_path = tmp_path / "video.mp4"
    dummy_path.write_text("dummy")

    metadata = build_local_placeholder_metadata(str(dummy_path))

    assert metadata["title"] == "video.mp4"
    assert metadata["duration"] is None
    assert metadata["author"] is None
    assert metadata["source_type"] == "file_system"
    assert metadata["source_path"] == str(dummy_path.resolve())
    assert metadata["source_url"] is None
    assert metadata["metadata_status"] == "incomplete"
    assert metadata["service_metadata"] == {}
