"""
Core audio extraction logic for YouTube videos.

Downloads the audio stream from a given YouTube URL and converts it to MP3 format.
"""
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from youtube_audio_extractor.retry import retry
from moviepy import VideoFileClip
import logging

@retry(max_attempts=3)
def download_audio(url, output_file):
    """
    Downloads audio from a YouTube video and saves it as an MP3 file.

    Parameters:
        url (str): The YouTube video URL.
        output_file (str): Path to save the resulting MP3 file.
    """
    logging.info(f"Starting download from URL: {url}")

    # Strip .mp3 if present
    if output_file.endswith(".mp3"):
        output_file = output_file[:-4]
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
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
            logging.info(f"Download complete: {output_file}")

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