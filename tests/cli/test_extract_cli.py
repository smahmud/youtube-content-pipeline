"""
File: test_extract_cli.py

Test suite for the 'extract' subcommand of the content-pipeline CLI.

Covers:
- Help output and argument parsing for the extract command
- Audio extraction from YouTube URLs and local video files
- Metadata enrichment and fallback behavior
- Error handling for missing or invalid extract arguments
- Output path resolution and file generation
"""

import subprocess
import sys
import os
import json
import shutil
from pathlib import Path
import pytest

CLI_PATH = os.path.abspath("main_cli.py")

TEST_OUTPUT_DIR = "tests/output"

@pytest.mark.integration
def test_cli_extract_help_output():
    result = subprocess.run([sys.executable, CLI_PATH, "extract", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Base filename for extracted audio (.mp3)" in result.stdout
    assert "--source" in result.stdout

@pytest.mark.integration
def test_cli_missing_arguments():
    """
    Verifies that the CLI exits with an error when required arguments are missing.
    """
    result = subprocess.run([
        sys.executable, CLI_PATH,         
          "extract"
          # No --source or --output provided
          ], capture_output=True, text=True)
    
    assert result.returncode != 0
    assert any(kw in result.stderr for kw in ["Missing argument", "Error:"])

def test_cli_extract_missing_input_file(tmp_path):
    missing_path = tmp_path / "nonexistent.mp4"
    output_path = tmp_path / "out.mp3"

    result = subprocess.run([
        sys.executable, CLI_PATH,
        "extract",
        "--source", str(missing_path), 
        "--output", str(output_path)
    ], capture_output=True, text=True)

    assert result.returncode != 0
    assert "Input file does not exist" in result.stdout or result.stderr

@pytest.mark.integration
def test_cli_extract_youtube_audio_and_metadata_extraction(tmp_path):
    """
    Verifies that the CLI downloads audio from a YouTube URL and saves both MP3 and metadata files.
    """
    output_path = tmp_path / "cli_download.mp3"
    metadata_path = output_path.with_suffix(".json")
    url = "https://www.youtube.com/watch?v=qcOiqtMsjes"

    result = subprocess.run([
        sys.executable, CLI_PATH,
        "extract",
        "--source", url,
        "--output", str(output_path)
    ], capture_output=True, text=True)

    assert result.returncode == 0
    assert output_path.exists()
    assert output_path.stat().st_size > 0

    # Validate metadata file
    assert metadata_path.exists()
    with open(metadata_path) as f:
        metadata = json.load(f)

        assert metadata["source_type"] == "youtube_url"
        assert metadata["source_url"] == url
        assert metadata["source_path"] is None
        assert metadata["metadata_status"] == "complete"
        assert isinstance(metadata["title"], str)
        assert isinstance(metadata["duration"], int)
        assert isinstance(metadata["author"], str)
        assert "service_metadata" in metadata
        assert isinstance(metadata["service_metadata"], dict)
        assert metadata["service_metadata"] != {}

    expected_keys = {
        "title", "duration", "author",
        "source_type", "source_path", "source_url",
        "metadata_status", "service_metadata"
    }
    assert expected_keys.issubset(metadata.keys())

    for path in [output_path, metadata_path]:
        if path.exists():
            path.unlink()

@pytest.mark.integration
def test_cli_extract_local_audio_and_placeholder_metadata(tmp_path):
    """
    Verifies that the CLI extracts audio from a local .mp4 file and generates placeholder metadata.
    """
    video_path = "tests/assets/sample_video.mp4"
    output_path = tmp_path / "cli_extracted.mp3"
    metadata_path = output_path.with_suffix(".json")

    result = subprocess.run([
        sys.executable, CLI_PATH,
        "extract",
        "--source", video_path,
        "--output", str(output_path)
    ], capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    assert result.returncode == 0
    assert output_path.exists()
    assert output_path.stat().st_size > 0

    # Validate placeholder metadata
    assert metadata_path.exists()
    with open(metadata_path) as f:
        metadata = json.load(f)
        assert metadata["title"] == os.path.basename(video_path)
        assert metadata["source_type"] == "file_system"
        assert metadata["source_path"] == os.path.abspath(video_path)
        assert metadata["source_url"] is None
        assert metadata["metadata_status"] == "incomplete"
        assert "service_metadata" in metadata
        assert isinstance(metadata["service_metadata"], dict)
        assert metadata["service_metadata"] == {}

    expected_keys = {
        "title", "duration", "author",
        "source_type", "source_path", "source_url",
        "metadata_status", "service_metadata"
    }
    assert expected_keys.issubset(metadata.keys())

    for path in [output_path, metadata_path]:
        if path.exists():
            path.unlink()
