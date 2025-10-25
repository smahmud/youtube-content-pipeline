"""
Command-line interface for the YouTube audio extractor.

Accepts a YouTube URL and an optional output filename, then triggers audio extraction and MP3 conversion.
"""

import click
from pytubefix import YouTube
from youtube_audio_extractor import extractor
import os
import logging

# Config logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

@click.command()
@click.argument("source")
@click.option("--output", default="output.mp3", help="Output filename")
def main(source, output):
    """
    CLI entry point for extracting audio from a YouTube video.

    Parameters:
        source (str): YouTube URL or path to local video file.
        output (str): Filename for the resulting MP3 file (default: output.mp3).
    """

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", output)

    if source.startswith("http"):
        try:
            extractor.download_audio(source, output_path)
            logging.info(f"Audio saved to: {output_path}")
        except Exception as e:
            logging.error(f"Failed to extract audio: {e}")
            print("Something went wrong. Please check the input and try again.")            
    else:
        extractor.extract_audio_from_file(source, output_path)
        
    print("\n Done. You may continue using the terminal.")

if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
    
