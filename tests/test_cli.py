"""
Test suite for the CLI entry point of the YouTube audio extraction pipeline.

Covers:
- Help output and argument parsing
- Functional dispatch to download and extract routines
- Error handling for invalid or missing arguments
"""

import subprocess
import sys
import os
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
    assert "Usage" in result.stdout or "--url" in result.stdout


@pytest.mark.integration
def test_cli_download_audio(tmp_path):
    """
    Verifies that the CLI downloads audio from a YouTube URL and saves it as an MP3 file.
    """
    output_path = tmp_path / "cli_download.mp3"
    url = "https://www.youtube.com/watch?v=qcOiqtMsjes"

    result = subprocess.run([
        sys.executable, CLI_PATH,
        url, 
        "--output", str(output_path)
    ], capture_output=True, text= True)

    assert result.returncode == 0
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    

@pytest.mark.integration
def test_cli_extract_audio_from_file(tmp_path):
    """
    Verifies that the CLI extracts audio from a local .mp4 file using the --extract flag.
    """    
    video_path = "tests/assets/sample_video.mp4"
    output_path = tmp_path / "cli_extracted.mp3"

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