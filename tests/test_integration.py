"""
test_integration.py

End-to-end integration tests for the content-pipeline project.

Covers:
- Real `.mp4` input and `.mp3` output generation
- Metadata extraction and persistence as `.json`
- CLI-driven execution across audio and metadata stages
- Schema validation and file existence checks
"""
import os
import json
import pytest
from pipeline.extractors.youtube.extractor import YouTubeExtractor
from pipeline.extractors.local.file_audio import extract_audio_from_file
from pipeline.extractors.local.metadata_utils import generate_local_placeholder_metadata

TEST_OUTPUT_DIR = "tests/outputs"

@pytest.mark.integration
def test_extract_audio_from_youtube_integration():
    """
    Integration test for download_audio_from_youtube() and extract_metadata_from_youtube().

    Downloads a real YouTube video and verifies that the audio and metadata files are created and valid.
    """
    
    source = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    output_path = os.path.join(TEST_OUTPUT_DIR, "test_download.mp3")
    metadata_path = output_path.replace(".mp3", ".json")

    try:        
        extractor = YouTubeExtractor()

        # Step 1: Download audio
        result_path = extractor.extract_audio(source, output_path)
        assert result_path.endswith(".mp3")
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
        
        # Step 2: Extract and save metadata
        metadata = extractor.extract_metadata(source)
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Validate metadata file
        assert os.path.exists(metadata_path)

        # Validate core schema
        assert metadata["source_type"] == "youtube_url"
        assert metadata["source_url"] == source
        assert metadata["source_path"] is None
        assert metadata["metadata_status"] == "complete"
        assert isinstance(metadata["title"], str)
        assert isinstance(metadata["duration"], int)
        assert isinstance(metadata["author"], str)

        # Validate service metadata
        assert "service_metadata" in metadata
        assert isinstance(metadata["service_metadata"], dict)
        assert "view_count" in metadata["service_metadata"] or "channel_id" in metadata["service_metadata"]

        # Validate full schema
        expected_keys = {
            "title", "duration", "author",
            "source_type", "source_path", "source_url",
            "metadata_status", "service_metadata"
        }
        assert expected_keys.issubset(metadata.keys())

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
        result_path = extract_audio_from_file(video_path, output_path)
        assert result_path.endswith(".mp3")

        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

        metadata_path = output_path.replace(".mp3", ".json")
        metadata = generate_local_placeholder_metadata(video_path)

        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        # Validate metadata file
        assert os.path.exists(metadata_path)

        # Validate core schema
        assert metadata["title"] == "sample_video.mp4"
        assert metadata["source_type"] == "local_file"
        assert metadata["source_path"] == os.path.abspath(video_path)
        assert metadata["source_url"] is None
        assert metadata["metadata_status"] == "incomplete"

        # Validate service metadata
        assert metadata["service_metadata"] == {}

        # Validate full schema
        expected_keys = {
            "title", "duration", "author",
            "source_type", "source_path", "source_url",
            "metadata_status", "service_metadata"
        }
        assert expected_keys.issubset(metadata.keys())

    finally:
        for path in [output_path, metadata_path]:
            if os.path.exists(path):
                os.remove(path)
