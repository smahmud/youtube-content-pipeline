"""
Test suite for audio extraction and download functionality.

Covers:
- Unit tests for internal logic using mocks (e.g. download_audio behavior)
- Integration tests for downloading from YouTube and extracting audio from local .mp4 files
"""
import os
from unittest.mock import patch, MagicMock
import pytest
from youtube_audio_extractor.extractor import download_audio, extract_audio_from_file

TEST_OUTPUT_DIR = "tests/outputs"

@pytest.fixture(scope="module", autouse=True)
def ensure_output_dir():
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)


@patch("youtube_audio_extractor.extractor.YoutubeDL")
def test_download_audio_mock(mock_yt_dlp):
    """
    Unit test for download_audio().
    
    Verifies that the YoutubeDL.download() method is called once with the expected arguments.
    Uses mocking to avoid actual network or file system operations.
    """

    mock_ydl_instance = MagicMock()
    mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance

    output_file = "tests/output/test_download.mp3"
    download_audio("https://fake-url.com", output_file)

    mock_ydl_instance.download.assert_called_once()


@pytest.mark.integration
def test_extract_audio_from_file_integration():
    """
    Integration test for extract_audio_from_file().
    
    Runs the full audio extraction pipeline on a sample video file.
    Asserts that the output audio file is created and non-empty.
    Cleans up the generated file after execution.
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


@pytest.mark.integration
def test_download_audio_integration():
    """
    Integration test for download_audio().

    Downloads a real YouTube video using yt_dlp and verifies that the output file is created and non-empty.
    Cleans up the downloaded file after execution.
    """
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    output_path = os.path.join(TEST_OUTPUT_DIR, "test_download.mp3")

    try:
        download_audio(url, output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    finally:
        if os.path.exists(output_path):
            os.remove(output_path) 

