"""
test_cli.py

Test suite for the CLI entry point of the YouTube audio extraction pipeline.

Covers:
- Help output and argument parsing
- Functional dispatch to download and extract routines
- Error handling for invalid or missing arguments
"""
import subprocess
import sys
import os
import json
import pytest
import shutil
from pathlib import Path
from unittest.mock import patch

CLI_PATH = os.path.abspath("cli.py")

TEST_OUTPUT_DIR = "tests/outputs"

@pytest.mark.integration
def test_cli_help_output():
    """
    Verifies that the CLI displays help text when invoked with --help.
    """
    result = subprocess.run([sys.executable, CLI_PATH, "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Usage" in result.stdout or "--url" in result.stdout


@pytest.mark.integration
def test_cli_missing_arguments():
    """
    Verifies that the CLI exits with an error when required arguments are missing.
    """
    result = subprocess.run([
        sys.executable, CLI_PATH,         
          # Missing input and output positional arguements
          ], capture_output=True, text=True)
    
    assert result.returncode != 0
    assert "error" in result.stderr.lower() or "missing" in result.stderr.lower()


def test_cli_missing_input_file(tmp_path):
    missing_path = tmp_path / "nonexistent.mp4"
    output_path = tmp_path / "out.mp3"

    result = subprocess.run([
        "python", "cli.py", 
        str(missing_path), 
        "--output", str(output_path)
    ], capture_output=True, text=True)

    assert result.returncode != 0
    assert "Input file does not exist" in result.stdout or result.stderr


def test_clic_invalid_metadata_url(tmp_path):
    input_path = tmp_path / "test_video.mp4"
    input_path.write_bytes(b"fake mp4 content")
    output_path = tmp_path / "out.mp3"

    result = subprocess.run([
        sys.executable, CLI_PATH,
        str(input_path), 
        "--output", str(output_path), 
        "--metadata-url", "https://not-a-real-url.com"
    ], capture_output=True, text=True)
    
    assert "Warning: Metadata enrichment failed" in result.stdout


@pytest.mark.integration
def test_cli_extract_audio_and_metadata_from_youtube(tmp_path):
    """
    Verifies that the CLI downloads audio from a YouTube URL and saves both MP3 and metadata files.
    """
    output_path = tmp_path / "cli_download.mp3"
    metadata_path = output_path.with_suffix(".json")
    url = "https://www.youtube.com/watch?v=qcOiqtMsjes"

    result = subprocess.run([
        sys.executable, CLI_PATH,
        url,
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
 

@pytest.mark.integration
def test_cli_extract_audio_and_placeholder_metadata_from_local_file(tmp_path):
    """
    Verifies that the CLI extracts audio from a local .mp4 file and generates placeholder metadata.
    """
    video_path = "tests/assets/sample_video.mp4"
    output_path = tmp_path / "cli_extracted.mp3"
    metadata_path = output_path.with_suffix(".json")

    result = subprocess.run([
        sys.executable, CLI_PATH,
        video_path,
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
        assert metadata["source_type"] == "local_file"
        assert metadata["source_path"] == os.path.abspath(video_path)
        assert metadata["source_url"] is None
        assert metadata["metadata_status"] == "incomplete"
        assert metadata["title"] == os.path.basename(video_path)

@pytest.mark.integration
def test_cli_extract_audio_and_enriched_metadata_from_local_file(tmp_path):
    """
    Verifies that the CLI extracts audio from a local file and enriches metadata using a YouTube URL.
    """
    # Use a real sample video file
    source_asset = Path("tests/assets/sample_video.mp4")
    input_path = tmp_path / "test_video.mp4"
    shutil.copy(source_asset, input_path)

    # Define output paths
    output_path = tmp_path / "test_output.mp3"
    metadata_path = output_path.with_suffix(".json")
    metadata_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    # Run CLI
    result = subprocess.run([
        sys.executable, CLI_PATH,
        str(input_path),
        "--output", str(output_path),
        "--metadata-url", metadata_url
    ], capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # Validate audio output
    assert result.returncode == 0
    assert output_path.exists()
    assert output_path.stat().st_size > 0

    # Validate metadata output
    assert metadata_path.exists()
    with open(metadata_path) as f:
        metadata = json.load(f)
        assert metadata["source_type"] == "local_file"
        assert metadata["source_path"] == str(input_path)
        assert metadata["source_url"] == metadata_url
        assert metadata["metadata_status"] == "complete"
        assert isinstance(metadata["title"], str)
        assert isinstance(metadata["duration"], int)
        assert isinstance(metadata["author"], str)

