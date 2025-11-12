"""
File: cli.py

Command-line interface for running the transcription pipeline.
Handles audio extraction, adapter selection, transcription, and output persistence.
"""
import os
import json
import sys
import logging
import click
from pipeline.extractors.youtube.extractor import YouTubeExtractor
from pipeline.extractors.dispatch import classify_source
from pipeline.extractors.schema.metadata import build_local_placeholder_metadata
from pipeline.extractors.local.file_audio import extract_audio_from_file
from pipeline.config.logging_config import configure_logging
from pipeline.transcribers.adapters.whisper import WhisperAdapter
from pipeline.transcribers.normalize import normalize_transcript_v1
from pipeline.transcribers.persistence import LocalFilePersistence

from cli.help_texts import (
    EXTRACT_SOURCE_HELP,
    EXTRACT_OUTPUT_HELP,
    TRANSCRIBE_SOURCE_HELP,
    TRANSCRIBE_OUTPUT_HELP,
    TRANSCRIBE_LANGUAGE_HELP
)

# Config logging
configure_logging()

# Now you can use logging as usual
logging.info("CLI started")

@click.group()
def cli():
    """Content Pipeline CLI"""
    pass

@cli.command()
@click.option("--source", required=True, help=EXTRACT_SOURCE_HELP)
@click.option("--output", default="output.mp3", help=EXTRACT_OUTPUT_HELP)
def extract(source, output):
    """
    Extract audio from the source file and save it to the specified output path.    
    """
    source_type = classify_source(source)
    
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", output)
    metadata_path = output_path.replace(".mp3", ".json")

    if source_type =="streaming":        
        extractor = YouTubeExtractor()
        try:
            metadata = extractor.extract_metadata(source)            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            logging.info(f"Metadata saved to: {metadata_path}")
        except Exception as e:
                logging.error(f"Failed to extract or save metadata: {e}")
                print("Warning: Metadata extraction failed.")

        try:
            extractor.extract_audio(source, output_path)
            logging.info(f"Audio saved to: {output_path}")
        except Exception as e:
            logging.error(f"Failed to extract audio: {e}")
            print("Warning: Audio extraction failed.")
    
    elif source_type == "storage":
        metadata = build_local_placeholder_metadata(source)
        try:
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            logging.info(f"Metadata saved to: {metadata_path}")
        except Exception as e:
            logging.error(f"Failed to save metadata: {e}")
            print("Warning: Could not save metadata.")

        # Placeholder for future extractor logic
        logging.warning("Cloud storage extraction not yet implemented.")

    else: # file_system
        if not os.path.exists(source):
            logging.error(f"Input file not found: {source}")
            print("Error: Input file does not exist.")
            sys.exit(1)

        metadata = build_local_placeholder_metadata(source)
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
            print("Warning: Audio extraction failed.")
        
    print("\n Done. You may continue using the terminal.")


@cli.command()
@click.option("--source", required=True, help=TRANSCRIBE_SOURCE_HELP)
@click.option("--output", default="transcript.json", help=TRANSCRIBE_OUTPUT_HELP)
@click.option("--language", default=None, help=TRANSCRIBE_LANGUAGE_HELP)
def transcribe(source, output, language):
    """
    Extract audio from the source, run transcription, and save the normalized transcript.
    """
    # Validate source file
    if not os.path.exists(source):
        logging.error(f"Audio file not found: {source}")
        print("Error: Audio file does not exist.")
        sys.exit(1)

    # Prepare output paths
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", output)

    # Run transcription
    adapter = WhisperAdapter(model_name="base")  # You can make model configurable later
    raw_transcript = adapter.transcribe(source, language=language)
    transcript = normalize_transcript_v1(raw_transcript, adapter)

    # Save transcript
    try:
        strategy = LocalFilePersistence()
        strategy.persist(transcript, output_path)
        logging.info(f"Transcript saved to: {output_path}")
    except Exception as e:
        logging.error(f"Failed to save transcript: {e}")
        print("Warning: Could not save transcript.")

    print("\n Done. Transcript generated.")

if __name__ == "__main__":
    cli()


