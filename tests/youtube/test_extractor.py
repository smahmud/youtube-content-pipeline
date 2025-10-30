"""
test_extractor.py

Test suite for audio extraction and download functionality.

Covers:
- Unit tests for internal logic using mocks (e.g. download_audio behavior)
- Metadata enrichment and fallback logic
- Schema validation for local and YouTube sources
"""
import os
from unittest.mock import patch, MagicMock
import pytest
from pipeline.extractors.youtube.extractor import YouTubeExtractor

TEST_OUTPUT_DIR = "tests/outputs"

@pytest.fixture(scope="module", autouse=True)
def ensure_output_dir():
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

@patch("pipeline.extractors.youtube.extractor.YoutubeDL")
def test_download_audio_from_youtube_triggers_download(mock_yt_dlp, tmp_path):
    mock_ydl_instance = MagicMock()
    mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance

    extractor = YouTubeExtractor()
    url = "https://youtube.com/watch?v=abc123"
    output_path = tmp_path / "test_output.mp3"

    result_path = extractor.extract_audio(url, str(output_path))

    mock_ydl_instance.download.assert_called_once_with([url])
    assert result_path.endswith(".mp3")
    assert "test_output" in result_path

@patch("pipeline.extractors.youtube.extractor.YoutubeDL")
def test_extract_metadata_from_youtube_returns_expected_structure(mock_yt_dlp):
    mock_yt_dlp.return_value.__enter__.return_value.extract_info.return_value = {
        "title": "Test Title",
        "duration": 123,
        "uploader": "Test Author",
        "view_count": 999,
        "channel_id": "UCabc123"        
    }

    extractor = YouTubeExtractor()
    source = "https://youtube.com/watch?v=abc123"
    metadata = extractor.extract_metadata(source)

    assert metadata["title"] == "Test Title"
    assert metadata["duration"] == 123
    assert metadata["author"] == "Test Author"
    assert metadata["source_type"] == "youtube_url"
    assert metadata["source_path"] is None
    assert metadata["source_url"] == source
    assert metadata["metadata_status"] == "complete"

    # Validate service_metadata
    assert "view_count" in metadata["service_metadata"]
    assert metadata["service_metadata"]["channel_id"] == "UCabc123"    