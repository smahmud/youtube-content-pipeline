"""
Core audio extraction logic for YouTube videos.

Downloads the audio stream from a given YouTube URL and converts it to MP3 format.
"""
from moviepy import VideoFileClip
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment
import ffmpeg
import os

def download_audio(url, output_file):
    """
    Downloads audio from a YouTube video and saves it as an MP3 file.

    Parameters:
        url (str): The YouTube video URL.
        output_file (str): Path to save the resulting MP3 file.
    """

    yt = YouTube(url, on_progress_callback=on_progress)    
    stream = yt.streams.filter(only_audio=True).first()
    temp_file = stream.download(filename="temp.mp4")
    audio = AudioSegment.from_file(temp_file)
    audio.export(output_file, format="mp3")
    print("✅ Audio extraction complete.")
    os.remove(temp_file)

def extract_audio_from_file(video_path: str, output_path:str) -> None:
    """
    Extracts audio from a local video file and saves it as an MP3.

    Parameters:
        video_path (str): Path to the local video file.
        output_path (str): Path to save the extracted MP3 file.
    """    
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio.write_audiofile(output_path)
    clip.close()
    print("Audio extraction from local file complete.")