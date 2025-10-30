"""
Command-line interface for the YouTube audio extractor.

Accepts a YouTube URL and an optional output filename, then triggers audio extraction and MP3 conversion.
"""
import os
import json
import sys
import logging
import click
from pipeline.extractors.youtube.extractor import YouTubeExtractor
from pipeline.extractors.local.metadata_utils import generate_local_placeholder_metadata
from pipeline.extractors.local.file_audio import extract_audio_from_file
from pipeline.config.logging_config import configure_logging

# Config logging
configure_logging()

# Now you can use logging as usual
logging.info("CLI started")

@click.command()
@click.argument("source")
@click.option("--output", default="output.mp3", help="Output filename")
@click.option("--metadata-url", type=str, help="YouTube URL to enrich metadata for a local video file")
def main(source, output, metadata_url):
    """
    CLI entry point for extracting audio from a YouTube video.

    Parameters:
        source (str): YouTube URL or path to local video file.
        output (str): Filename for the resulting MP3 file (default: output.mp3).
    """

    if not source.startswith("http") and not os.path.exists(source):
        logging.error(f"Input file not found: {source}")
        print("Error: Input file does not exist.")
        sys.exit(1)

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", output)
    metadata_path = output_path.replace(".mp3", ".json")

    extractor = YouTubeExtractor()

    if source.startswith("http"):
        # Youtube flow
        try:            
            metadata = extractor.extract_metadata(source)            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            logging.info(f"Metadata saved to: {metadata_path}")
        except Exception as e:
                logging.error(f"Failed to extract or save metadata: {e}")
                logging.warning("Metadata extraction failed.")

        try:
            extractor.extract_audio(source, output_path)
            logging.info(f"Audio saved to: {output_path}")
        except Exception as e:
            logging.error(f"Failed to extract audio: {e}")
            logging.warning("Something went wrong. Please check the input and try again.")            
    else:
        # Local file flow
        if metadata_url:
            #metadata_path = output_path.replace(".mp3", ".json")
            try:
                metadata = extractor.extract_metadata(metadata_url)
                metadata["source_type"] = "local_file"
                metadata["source_path"] = os.path.abspath(source)
                metadata["source_url"] = metadata_url
                metadata["metadata_status"] = "complete"
                logging.info(f"Metadata enriched from URL: {metadata_url}")
            except Exception as e:
                logging.info(f"Metadata enrichment failed: {e}")
                print("Warning: Metadata enrichment failed. Falling back to placeholder.")
                metadata = generate_local_placeholder_metadata(source)
        else:
            metadata = generate_local_placeholder_metadata(source)

        try:
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            logging.info(f"Metadata saved to: {metadata_path}")
        except Exception as e:
            logging.error(f"Failed to save metadata: {e}")
            print("Warning: Could not save metadata.")

        try:
            extract_audio_from_file(source, output_path)
            logging.info(f"Audio extracted from local file: {output_path}")
        except Exception as e:
            logging.error(f"Failed to extract audio from local file: {e}")            
            print("Audio extraction failed.")
        
    print("\n Done. You may continue using the terminal.")

if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
    
