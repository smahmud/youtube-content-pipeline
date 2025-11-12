"""
File: extractor.py

Audio and metadata extraction logic for YouTube sources in the content-pipeline project.

Implements a YouTubeExtractor that uses yt_dlp to download audio and retrieve structured metadata.
Supports retry logic and schema normalization for downstream enrichment and transcription workflows.
"""
import logging
from pathlib import Path
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from pipeline.utils.retry import retry
from pipeline.extractors.base import BaseExtractor
from pipeline.extractors.schema.metadata import build_base_metadata

class YouTubeExtractor(BaseExtractor):
    """
    Extractor for YouTube sources using yt_dlp.

    Provides methods to download audio and extract metadata from YouTube URLs.
    Used by CLI and orchestration layers to support streaming workflows.
    """
    @retry(max_attempts=3)
    def extract_audio(self, source: str, output_path: str) -> str:
        """
        Downloads audio from a YouTube video and saves it as an MP3 file.

        Automatically strips the .mp3 extension from the output path to avoid duplication.
        The resulting file is saved as <output_path>.mp3.
        """
        logging.info(f"[extract_audio] Starting download from: {source}")        

        output_path = Path(output_path)
        if output_path.suffix == ".mp3":
            output_path = output_path.with_suffix("")
        
        audio_path = output_path.with_suffix(".mp3")

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
                ydl.download([source])
                logging.info(f"[extract_audio] Download complete: {audio_path}")
                return str(audio_path)

        except DownloadError as e:
            logging.error(f"[extract_audio] Download failed: {e}")
            raise RuntimeError(f"[extract_audio] Download failed: {e}")

    @retry(max_attempts=3)
    def extract_metadata(self, source: str) -> dict:
        """
        Extracts metadata from a YouTube video using yt_dlp.

        Returns a dictionary with title, duration, author, and source information.
        """
        logging.info(f"[extract_metadata] Starting metadata extraction from: {source}")

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "forcejson": True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(source, download=False)
                if not info:
                    raise ValueError("No metadata returned from yt_dlp")

                metadata = build_base_metadata(
                    title=info.get("title"),
                    duration=info.get("duration"),
                    author=info.get("uploader"),
                    source_type="streaming",
                    source_path=None,
                    source_url=source,
                    metadata_status="complete",
                    service_metadata={
                        "view_count": info.get("view_count"),
                        "channel_id": info.get("channel_id")
                    }
                )
            
                logging.info(f"[extract_metadata] Extraction complete for: {source}")
                return metadata
        except Exception as e:
            logging.error(f"[extract_metadata] Metadata extraction failed: {e}")
            raise RuntimeError(f"[extract_metadata] Metadata extraction failed: {e}")
