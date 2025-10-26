"""
Core audio extraction logic for YouTube videos.

Downloads the audio stream from a given YouTube URL and converts it to MP3 format.
"""
import logging
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from moviepy import VideoFileClip
from youtube_audio_extractor.retry import retry

@retry(max_attempts=3)
def download_audio(url: str, output_path: str) -> None:
    """
    Downloads audio from a YouTube video and saves it as an MP3 file.

    Automatically strips the .mp3 extension from the output path to avoid duplication.
    The resulting file is saved as <output_path>.mp3.
    """

    logging.info(f"Starting download from URL: {url}")

    # Strip .mp3 if present
    if output_path.endswith(".mp3"):
        output_path = output_path[:-4]
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
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
            ydl.download([url])
            logging.info(f"Download complete: {output_path}")

    except DownloadError as e:
        logging.error(f"Failed to extract audio: {e}")
        raise RuntimeError(f"Download failed: {e}")
        

@retry(max_attempts=3)
def extract_audio_from_file(video_path: str, output_path:str) -> None:
    """
    Extracts audio from a local video file and saves it as an MP3.

    Parameters:
        video_path (str): Path to the local video file.
        output_path (str): Path to save the extracted MP3 file.
    """    
    logging.info(f"Extracting audio from: {video_path}")
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio.write_audiofile(output_path)
    clip.close()
    logging.info(f"Audio saved to: {output_path}")
    print("Audio extraction from local file complete.")