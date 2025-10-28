"""
Command-line interface for the YouTube audio extractor.

Accepts a YouTube URL and an optional output filename, then triggers audio extraction and MP3 conversion.
"""
import logging
from youtube_audio_extractor.logging_config import configure_logging
import os
import json
import sys
import click
from youtube_audio_extractor import extractor


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

    if source.startswith("http"):
        # Step 1: Extract metadata        
        metadata_path = output_path.replace(".mp3", ".json")        
        try:            
            metadata = extractor.extract_metadata_from_youtube(source)            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            logging.info(f"Metadata saved to: {metadata_path}")
        except Exception as e:
                logging.error(f"Failed to extract or save metadata: {e}")
                logging.warning("Metadata extraction failed.")

        # Step 2: Extract audio
        try:
            extractor.download_audio_from_youtube(source, output_path)
            logging.info(f"Audio saved to: {output_path}")
        except Exception as e:
            logging.error(f"Failed to extract audio: {e}")
            logging.warning("Something went wrong. Please check the input and try again.")            
    else:        
        metadata_path = output_path.replace(".mp3", ".json")

        if metadata_url:
            try:
                metadata = extractor.extract_metadata(metadata_url)
                metadata["source_type"] = "local_file"
                metadata["source_path"] = os.path.abspath(source)
                metadata["source_url"] = metadata_url
                metadata["metadata_status"] = "complete"
                logging.info(f"Metadata enriched from URL: {metadata_url}")
            except Exception as e:
                logging.info(f"Failed to extract metadata from {metadata_url} : {e}")
                print("Warning: Metadata enrichment failed. Falling back to placeholder.")
                metadata = extractor.generate_placeholder_metadata(source)
        else:
            metadata = extractor.generate_placeholder_metadata(source)

        try:

            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            logging.info(f"Placeholder metadata saved to: {metadata_path}")
        except Exception as e:
            logging.error(f"Failed to save placeholder metadata: {e}")
            print("Warning: Could not save placeholder metadata.")

        try:
            extractor.extract_audio_from_file(source, output_path)
            logging.info(f"Audio extracted from local file: {output_path}")
        except Exception as e:
            logging.error(f"Failed to extract audio from local file: {e}")
            print("Something went wrong during audio extraction. Please check the file and try again.")
        
    print("\n Done. You may continue using the terminal.")

if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
    
