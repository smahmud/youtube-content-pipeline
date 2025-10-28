"""
Core audio extraction logic for YouTube videos.

Downloads the audio stream from a given YouTube URL and converts it to MP3 format.
"""
import logging
import os
import json
from pathlib import Path
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from moviepy import VideoFileClip
from youtube_audio_extractor.retry import retry

@retry(max_attempts=3)
def download_audio_from_youtube(url: str, output_path: str) -> None:
    """
    Downloads audio from a YouTube video and saves it as an MP3 file.
    """
    logging.info(f"Starting download from URL: {url}")

    output_path = Path(output_path)

    if output_path.suffix == ".mp3":
        output_path = output_path.with_suffix("")

    audio_path = output_path.with_suffix(".mp3")
    metadata_path = output_path.with_suffix(".json")
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Download audio
            ydl.download([url])
            logging.info(f"Download complete: {audio_path}")

    except DownloadError as e:
        logging.error(f"Audio download failed: {e}")
        raise RuntimeError(f"Audio download failed: {e}")  


@retry(max_attempts=3)
def extract_metadata_from_youtube(url: str) -> dict:
    """
    Extracts metadata from a YouTube video using yt_dlp.
    Returns title, duration (in seconds), and author.
    """
    logging.info(f"Extracting metadata from URL: {url}")

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise ValueError("No metadata returned from yt_dlp")

            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "author": info.get("uploader"),
                "source_type": "youtube_url",
                "source_path": None,
                "source_url": url,
                "metadata_status": "complete"
            }
    except Exception as e:
        logging.error(f"Metadata extraction failed: {e}")
        raise RuntimeError(f"Metadata extraction failed: {e}")


@retry(max_attempts=3)
def extract_audio_from_file(video_path: str, output_path:str) -> None:
    """
    Extracts audio from a local video file and saves it as an MP3.

    Parameters:
        video_path (str): Path to the local video file.
        output_path (str): Path to save the extracted MP3 file.
    """    
    # Enforce .mp3 extension for audio file
    if not output_path.endswith(".mp3"):
        output_path += ".mp3"

    try:
        clip = VideoFileClip(video_path)
        if not clip.audio:
            raise ValueError("No audio track found.")
        
        clip.audio.write_audiofile(output_path)
        logging.info(f"Audio saved to: {output_path}")
        print("Audio extraction from local file complete.")
    except Exception as e:
        logging.info(f"Audio extraction failed for {video_path} : {e}")
        raise
    finally:
        if clip:
            clip.close()


def extract_metadata(url: str) -> dict:
    """
    Extracts metadata from a YouTube video using yt_dlp.
    Returns title, duration (in seconds), and author.
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "author": info.get("uploader"),
            "source_type": "youtube_url",
            "source_path": None,   # No local file path in this context
            "source_url": url,
            "metadata_status": "complete",
        }


def generate_placeholder_metadata(file_path: str) -> dict:
    return {
        "title": Path(file_path).name,
        "duration": None,
        "author": None,
        "source_type": "local_file",
        "source_path": os.path.abspath(file_path),
        "source_url": None,
        "metadata_status": "incomplete",
    }