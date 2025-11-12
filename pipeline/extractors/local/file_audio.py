"""
File: local_audio.py

Audio extraction utilities for file-system sources in the content-pipeline project.

Provides conversion from video to audio for locally accessible media files.
Used by CLI and orchestration layers to support transcription, enrichment, and archival workflows.
"""
from moviepy import VideoFileClip

def extract_audio_from_file(video_path: str, output_path: str) -> str:
    """
    Extracts audio from a local video file and writes it to the specified output path.
    """
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_path)
    clip.close()
    return output_path

