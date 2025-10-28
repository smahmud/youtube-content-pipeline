"""
test_extractor.py

Test suite for audio extraction and download functionality.

Covers:
- Unit tests for internal logic using mocks (e.g. download_audio behavior)
- Metadata enrichment and fallback logic
- Schema validation for local and YouTube sources
"""
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from youtube_audio_extractor.extractor import download_audio_from_youtube, extract_metadata_from_youtube, extract_audio_from_file, extract_metadata, generate_placeholder_metadata

TEST_OUTPUT_DIR = "tests/outputs"

@pytest.fixture(scope="module", autouse=True)
def ensure_output_dir():
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)


@patch("youtube_audio_extractor.extractor.YoutubeDL")
def test_download_triggers_youtubedl_smoke(mock_yt_dlp, tmp_path):
    mock_ydl_instance = MagicMock()
    mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance
    mock_ydl_instance.extract_info.return_value = {"title": "T", "duration": 1, "uploader": "U"}

    url = "https://youtube.com/watch?v=abc123"
    output_path = "test_output.mp3"

    download_audio_from_youtube(url, output_path)

    mock_ydl_instance.download.assert_called_once()


@patch("youtube_audio_extractor.extractor.YoutubeDL")
def test_download_audio_from_youtube_triggers_download(mock_yt_dlp):
    mock_ydl_instance = MagicMock()
    mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance

    url = "https://youtube.com/watch?v=abc123"
    output_path = "test_output.mp3"

    download_audio_from_youtube(url, output_path)

    mock_ydl_instance.download.assert_called_once_with([url])


@patch("youtube_audio_extractor.extractor.YoutubeDL")
def test_extract_metadata_from_youtube_returns_expected_structure(mock_yt_dlp):
    mock_yt_dlp.return_value.__enter__.return_value.extract_info.return_value = {
        "title": "Test Title",
        "duration": 123,
        "uploader": "Test Author"
    }

    url = "https://youtube.com/watch?v=abc123"
    metadata = extract_metadata_from_youtube(url)

    assert metadata == {
        "title": "Test Title",
        "duration": 123,
        "author": "Test Author",
        "source_type": "youtube_url",
        "source_path": None,
        "source_url": url,
        "metadata_status": "complete"
    }


@patch("youtube_audio_extractor.extractor.VideoFileClip")
def test_extract_audio_from_file_calls_write_audiofile(mock_video_clip):
    # Setup mock clip and audio
    mock_audio = MagicMock()
    mock_clip = MagicMock()
    mock_clip.audio = mock_audio
    mock_video_clip.return_value = mock_clip

    video_path = "dummy_video.mp4"
    output_path = "output.mp3"

    extract_audio_from_file(video_path, output_path)

    # Assert VideoFileClip was called with the video path
    mock_video_clip.assert_called_once_with(video_path)

    # Assert write_audiofile was called with the correct output path
    mock_audio.write_audiofile.assert_called_once_with(output_path)

    # Assert clip was closed
    mock_clip.close.assert_called_once()


def test_generate_placeholder_metadata_returns_expected_structure(tmp_path):
    # Create a dummy file path
    dummy_path = tmp_path / "video.mp4"

    # Generate metadata
    metadata = generate_placeholder_metadata(str(dummy_path))

    # Validate structure and values
    assert metadata["title"] == "video.mp4"
    assert metadata["duration"] is None
    assert metadata["author"] is None
    assert metadata["source_type"] == "local_file"
    assert metadata["source_path"] == str(dummy_path.resolve())
    assert metadata["source_url"] is None
    assert metadata["metadata_status"] == "incomplete"

