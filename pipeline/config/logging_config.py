"""
Centralized logging configuration for the content-pipeline project.

Defines consistent logging format, levels, and handlers across CLI, extractors, and agents.
Supports modular observability and integration with future MCP and GUI components.
"""
import logging
import sys

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )