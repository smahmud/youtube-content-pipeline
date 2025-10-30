"""
Utilities for extracting, validating, and persisting media metadata in the content-pipeline project.

Supports structured metadata generation from YouTube and local sources.
Ensures consistency across enrichment, logging, and downstream processing stages.
"""
from pathlib import Path
from pipeline.schema.metadata import build_base_metadata

def generate_local_placeholder_metadata(file_path: str) -> dict:
    path = Path(file_path).resolve()
    return build_base_metadata(
        title=path.name,
        duration=None,
        author=None,
        source_type="local_file",
        source_path=str(path),
        source_url=None,
        metadata_status="incomplete"
    )
