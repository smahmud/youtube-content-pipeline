"""
File: metadata.py

Defines the metadata schema used across the content-pipeline project.

Provides structured representations for media metadata extracted from streaming services and local/cloud sources.
Ensures consistency and validation for downstream enrichment, transcription, and archival stages.
"""
from typing import Optional, Dict, Literal
from pathlib import Path
from pipeline.extractors.dispatch import classify_source

def build_base_metadata(
    title: str,
    duration: Optional[int],
    author: Optional[str],
    source_type: Optional[str],
    source_path: Optional[str],
    source_url: Optional[str],
    metadata_status: Literal["complete", "incomplete"],
    service_metadata: Optional[Dict] = None
) -> dict:
    """
    Constructs a normalized metadata dictionary for any media source.
    """
    return {
        "title": title,
        "duration": duration,
        "author": author,
        "source_type": source_type,
        "source_path": source_path,
        "source_url": source_url,
        "metadata_status": metadata_status,
        "service_metadata": service_metadata or {}
    }

def build_local_placeholder_metadata(file_path: str) -> dict:
    """
    Generates minimal metadata for a local or cloud-based file reference.
    Classification is delegated to dispatch.classify_source().
    """
    source_type = classify_source(file_path)

    if source_type == "file_system":
        path = Path(file_path).resolve()
        title = path.name
        source_path = str(path)
    else:
        title = Path(file_path).name
        source_path = file_path

    return build_base_metadata(
        title=title,
        duration=None,
        author=None,
        source_type=source_type,
        source_path=source_path,
        source_url=None,
        metadata_status="incomplete"
    )
