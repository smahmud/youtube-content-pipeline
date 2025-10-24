"""
Command-line interface for the YouTube audio extractor.

Accepts a YouTube URL and an optional output filename, then triggers audio extraction and MP3 conversion.
"""

import click
from pytubefix import YouTube
from youtube_audio_extractor import extractor
import os

@click.command()
@click.argument("url")
@click.option("--output", default="output.mp3", help="Output filename")
def main(url, output):
    """
    CLI entry point for extracting audio from a YouTube video.

    Parameters:
        url (str): The YouTube video URL to process.
        output (str): The filename for the resulting MP3 file (default: output.mp3).
    """

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", output)
    extractor.download_audio(url, output_path)
    print("\n🎯 Done. You may continue using the terminal.")

if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
    
