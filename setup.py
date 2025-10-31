
"""
setup.py — Packaging metadata and CLI entry point for content-pipeline.

Version: 0.4.0 — Multi-agent architecture overhaul
"""
from setuptools import setup, find_packages

setup(
    name="content-pipeline",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        "yt_dlp",
        "click",
        "moviepy",
    ],
    entry_points={
        "console_scripts": [
            "extract-audio=cli:main",
        ],
    },
    python_requires=">=3.8",
)