"""
setup.py

Packaging metadata and CLI entry point for the content-pipeline.

Version: 0.5.0 — Adds transcription and normalization via Whisper adapter,
complementing prior audio extraction functionality. CLI refactored into modular
subcommands for extract and transcribe.
"""
from setuptools import setup, find_packages

setup(
    name="content-pipeline",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[
        "yt_dlp",
        "click",
        "moviepy",
        "pydantic>=2.0",
        "ffmpeg-python",
        "openai-whisper",
    ],
    entry_points={
        "console_scripts": [
            "content-pipeline=content_pipeline.cli:cli",
        ],
    },
    python_requires=">=3.8",
)