"""
File: help_texts.py

Centralized help text definitions for CLI options and arguments.
Used across Click commands to ensure consistent contributor-facing descriptions.
"""

EXTRACT_SOURCE_HELP = (
    "Streaming platform URL (currently only YouTube) or a YouTube video file (.mp4) in the local file system. "
    "Future support includes Vimeo, TikTok, and cloud-hosted video files."
)

EXTRACT_OUTPUT_HELP = (
    "Base filename for extracted audio (.mp3) and its metadata (.json). "
    "Currently saved to the local file system; future support includes cloud destinations."
)

TRANSCRIBE_SOURCE_HELP = (
    "Path to an audio file (.mp3) in the local file system. "
    "Future support includes cloud-hosted audio files."
)

TRANSCRIBE_OUTPUT_HELP = (
    "Base filename for transcript (.json) generated from audio. Uses TranscriptV1 schema. "
    "Currently saved to the local file system; future support includes cloud destinations."
)

TRANSCRIBE_LANGUAGE_HELP = (
    "Optional language hint for transcription (e.g., 'en', 'fr'). "
    "Improves accuracy when language is known. If omitted, language will be auto-detected."
)

