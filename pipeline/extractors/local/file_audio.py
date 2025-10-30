"""
Local audio extraction utilities for the content-pipeline project.

Handles conversion and validation of audio files from local sources.
Supports .mp4 to .mp3 extraction for downstream transcription and enrichment stages.
Designed for modular integration with CLI and MCP orchestration.
"""
from moviepy import VideoFileClip

def extract_audio_from_file(video_path: str, output_path: str) -> str:
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_path)
    clip.close()
    return output_path
