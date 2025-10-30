"""
test_metadata_utils.py

Unit tests for metadata extraction utilities.

Covers:
- Structured metadata output from YouTube sources
- yt_dlp behavior and fallback logic
- Schema compliance for enrichment and archival stages
"""
from pipeline.extractors.local.metadata_utils import generate_local_placeholder_metadata

def test_generate_placeholder_metadata_returns_expected_structure(tmp_path):
    dummy_path = tmp_path / "video.mp4"
    dummy_path.write_text("dummy")

    metadata = generate_local_placeholder_metadata(str(dummy_path))

    assert metadata["title"] == "video.mp4"
    assert metadata["duration"] is None
    assert metadata["author"] is None
    assert metadata["source_type"] == "local_file"
    assert metadata["source_path"] == str(dummy_path.resolve())
    assert metadata["source_url"] is None
    assert metadata["metadata_status"] == "incomplete"

    # Validate service_metadata is empty
    assert metadata["service_metadata"] == {}