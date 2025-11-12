"""
File: logging_config.py

Logging configuration for the content-pipeline project.

Establishes a consistent logging format and output stream across CLI, extractors, and orchestration layers.
Supports modular observability and future integration with MCP and GUI components.
"""
import logging
import sys

def configure_logging():
    """
    Configures global logging with standardized format and INFO-level output to stdout.
    """    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )