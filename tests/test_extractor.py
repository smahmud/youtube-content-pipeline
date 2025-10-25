import os
import pytest
from youtube_audio_extractor.extractor import download_audio, extract_audio_from_file

TEST_OUTPUT_DIR = "tests/outputs"

@pytest.mark.parametrize("url", [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
])

def test_download_audio(url):
    output_file = os.path.join(TEST_OUTPUT_DIR, "test_download.mp3")
    try:
        download_audio(url, output_file)
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

def test_extract_audio_from_file():
    video_path = "tests/assets/sample_video.mp4" # Provide a small test video here
    output_path = os.path.join(TEST_OUTPUT_DIR, "test_audio.mp3")
    try:
        extract_audio_from_file(video_path, output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
