"""
test_cli.py

Test suite for the CLI entry point of the content-pipeline project.

Covers:
- Help output and argument parsing via Click
- Dispatch to audio extraction and metadata routines
- Error handling for missing or invalid arguments
- CLI flags and output path resolution
"""
import subprocess
import sys
import os
import json
import shutil
from pathlib import Path
import pytest

CLI_PATH = os.path.abspath("cli.py")

TEST_OUTPUT_DIR = "tests/outputs"

@pytest.mark.integration
def test_cli_help_output():
    """
    Verifies that the CLI displays help text when invoked with --help.
    """
    result = subprocess.run([sys.executable, CLI_PATH, "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Output filename" in result.stdout  # from --output help

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
    assert any(kw in result.stderr for kw in ["Missing argument", "Error:"])

def test_cli_missing_input_file(tmp_path):
    missing_path = tmp_path / "nonexistent.mp4"
    output_path = tmp_path / "out.mp3"

    result = subprocess.run([
        sys.executable, CLI_PATH,
        str(missing_path), 
        "--output", str(output_path)
    ], capture_output=True, text=True)

    assert result.returncode != 0
    assert "Input file does not exist" in result.stdout or result.stderr

def test_cli_invalid_metadata_url_fallback(tmp_path):
    input_path = tmp_path / "test_video.mp4"
    output_path = tmp_path / "out.mp3"

    result = subprocess.run([
        sys.executable, CLI_PATH,
        str(input_path), 
        "--output", str(output_path), 
        "--metadata-url", "https://not-a-real-url.com"
    ], capture_output=True, text=True)
    
    assert any("Input file does not exist" in stream for stream in [result.stdout, result.stderr])

@pytest.mark.integration
def test_cli_youtube_audio_and_metadata_extraction(tmp_path):
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
def test_cli_local_audio_and_placeholder_metadata(tmp_path):
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
        assert metadata["title"] == os.path.basename(video_path)
        assert metadata["source_type"] == "local_file"
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

@pytest.mark.integration
def test_cli_local_audio_with_metadata_enrichment(tmp_path):
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

