"""
Defines the metadata schema used across the content-pipeline project.

Provides structured representations for media metadata extracted from YouTube and local sources.
Ensures consistency and validation for downstream enrichment, transcription, and archival stages.
"""

from typing import Optional, Dict, Literal

SourceType = Literal["youtube_url", "local_file"]

def build_base_metadata(
    title: str,
    duration: Optional[int],
    author: Optional[str],
    source_type: SourceType,
    source_path: Optional[str],
    source_url: Optional[str],
    metadata_status: Literal["complete", "incomplete"],
    service_metadata: Optional[Dict] = None
) -> dict:
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