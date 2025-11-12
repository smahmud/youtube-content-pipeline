"""
File: test_file_audio.py

Unit tests for local audio extraction logic.

Covers:
- Mocked .mp4 to .mp3 conversion using VideoFileClip
- Method call verification and return value assertions
- Isolation from real file I/O
"""
from unittest.mock import patch, MagicMock
from pipeline.extractors.local.file_audio import extract_audio_from_file

@patch("pipeline.extractors.local.file_audio.VideoFileClip")
def test_extract_audio_from_file_calls_write_audiofile(mock_video_clip):
    mock_audio = MagicMock()
    mock_clip = MagicMock()
    mock_clip.audio = mock_audio
    mock_video_clip.return_value = mock_clip

    video_path = "dummy_video.mp4"
    output_path = "output.mp3"

    result = extract_audio_from_file(video_path, output_path)

    mock_video_clip.assert_called_once_with(video_path)
    mock_audio.write_audiofile.assert_called_once_with(output_path)
    mock_clip.close.assert_called_once()
    assert result == output_path
