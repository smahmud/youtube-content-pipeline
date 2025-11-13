"""
File: test_transcribe_cli.py

Test suite for the 'transcribe' subcommand of the content-pipeline CLI.

Covers:
- Help output and argument parsing for the transcribe command
- Audio transcription using the Whisper adapter
- Language override behavior
- Raw output passthrough and schema normalization
- Transcript validation and persistence
- Error handling for missing files or invalid inputs
"""

import subprocess
import sys
import os
import json
import pytest

CLI_PATH = os.path.abspath("main_cli.py")

TEST_OUTPUT_DIR = "tests/output"

@pytest.mark.integration
def test_cli_transcribe_help_output():
    result = subprocess.run([sys.executable, CLI_PATH, "transcribe", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "--source" in result.stdout
    assert "--output" in result.stdout
    assert "--language" in result.stdout

@pytest.mark.integration
def test_cli_transcribe_local_audio(tmp_path):
    """
    Verifies that the CLI transcribes a local MP3 file and saves a valid transcript.
    """
    from shutil import copyfile
    input_audio = tmp_path / "sample.mp3"
    copyfile("tests/assets/sample_audio.mp3", input_audio)

    output_path = tmp_path / "output" / "transcript.json"

    result = subprocess.run([
        sys.executable, CLI_PATH,
        "transcribe",
        "--source", str(input_audio),
        "--output", str(output_path.name)
    ], cwd=tmp_path, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    assert result.returncode == 0
    assert output_path.exists()
    with open(output_path) as f:
        data = json.load(f)
        assert "metadata" in data
        assert "transcript" in data
        assert isinstance(data["transcript"], list)

@pytest.mark.integration
def test_cli_transcribe_output_structure(tmp_path):
    from shutil import copyfile
    input_audio = tmp_path / "sample.mp3"
    copyfile("tests/assets/sample_audio.mp3", input_audio)

    result = subprocess.run([
        sys.executable, CLI_PATH,
        "transcribe",
        "--source", str(input_audio)
    ], cwd=tmp_path, capture_output=True, text=True)

    output_path = tmp_path / "output" / "transcript.json"
    assert output_path.exists()

    with open(output_path) as f:
        data = json.load(f)
        assert isinstance(data, dict)
        assert "metadata" in data
        assert "transcript" in data
        assert isinstance(data["transcript"], list)
        assert all("text" in segment for segment in data["transcript"])

@pytest.mark.integration
def test_cli_transcribe_with_language_flag(tmp_path):
    from shutil import copyfile
    input_audio = tmp_path / "sample.mp3"
    copyfile("tests/assets/sample_audio.mp3", input_audio)

    result = subprocess.run([
        sys.executable, CLI_PATH,
        "transcribe",
        "--source", str(input_audio),
        "--language", "en"
    ], cwd=tmp_path, capture_output=True, text=True)

    output_path = tmp_path / "output" / "transcript.json"
    assert output_path.exists()

    with open(output_path) as f:
        data = json.load(f)
        assert "metadata" in data
        assert data["metadata"].get("language") == "en"


