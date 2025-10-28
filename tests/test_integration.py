"""
test_integration.py

End-to-end integration tests for the YouTube audio extraction pipeline.

Covers:
- Full pipeline behavior with real inputs
- Audio and metadata file generation
- Schema compliance and traceability
"""
import os
import json
from unittest.mock import patch, MagicMock
import pytest
from youtube_audio_extractor.extractor import download_audio_from_youtube, extract_metadata_from_youtube, extract_audio_from_file
TEST_OUTPUT_DIR = "tests/outputs"

@pytest.mark.integration
def test_extract_audio_from_youtube_integration():
    """
    Integration test for download_audio_from_youtube() and extract_metadata_from_youtube().

    Downloads a real YouTube video and verifies that the audio and metadata files are created and valid.
    """
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    output_path = os.path.join(TEST_OUTPUT_DIR, "test_download.mp3")
    metadata_path = output_path.replace(".mp3", ".json")

    try:
        # Step 1: Download audio
        download_audio_from_youtube(url, output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
        
        # Step 2: Extract and save metadata
        metadata = extract_metadata_from_youtube(url)
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        # Validate metadata
        assert os.path.exists(metadata_path)
        assert metadata["source_type"] == "youtube_url"
        assert metadata["source_url"] == url
        assert metadata["source_path"] is None
        assert metadata["metadata_status"] == "complete"
        assert isinstance(metadata["title"], str)
        assert isinstance(metadata["duration"], int)
        assert isinstance(metadata["author"], str)

    finally:
        for path in [output_path, metadata_path]:
            if os.path.exists(path):
                os.remove(path)


@pytest.mark.integration
def test_extract_audio_from_file_integration():
    """
    Integration test for extract_audio_from_file().

    Verifies that audio is extracted from a local video file and saved as an MP3.
    """
    video_path = "tests/assets/sample_video.mp4"
    output_path = os.path.join(TEST_OUTPUT_DIR, "test_audio.mp3")

    try:
        extract_audio_from_file(video_path, output_path)

        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


