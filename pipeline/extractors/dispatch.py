"""
File: dispatch.py

Dispatch logic for classifying media sources in the content-pipeline project.

Provides centralized routing for source type detection across local files, streaming services,
and cloud storage providers. Used by CLI and orchestration layers to determine appropriate
extractor and metadata strategy.

Supports:
- Provider-agnostic classification via URI scheme and domain matching
- Extensible registries for streaming and storage services
- Future-proof separation of local, remote, and streaming flows

Example usage:
    classify_source("s3://my-bucket/video.mp4") → "storage"
    classify_source("https://youtube.com/watch?v=abc") → "streaming"
    classify_source("/home/user/video.mp4") → "file_system"
"""
from urllib.parse import urlparse
from typing import Literal

# Step 1: Known streaming domains
STREAMING_DOMAINS = {
    "youtube.com",
    "youtu.be",
    "vimeo.com",
    "tiktok.com"
}

# Step 2: Known storage schemes and domains
STORAGE_SCHEMES = {"s3", "gs", "azure", "oci"}
STORAGE_DOMAINS = {
    "s3.amazonaws.com",
    "storage.googleapis.com",
    "blob.core.windows.net",
    "objectstorage.oraclecloud.com",
    "onedrive.live.com",
    "drive.google.com",
    "icloud.com"
}

# Step 3: Dispatch logic
def classify_source(source: str) -> Literal["streaming", "storage", "file_system"]:
    """
    Determines the source type based on URI scheme and domain characteristics.
    """
    parsed = urlparse(source)
    scheme = parsed.scheme
    netloc = parsed.netloc

    if scheme in ("http", "https"):
        if any(domain in netloc for domain in STREAMING_DOMAINS):
            return "streaming"
        if any(domain in netloc for domain in STORAGE_DOMAINS):
            return "storage"
    elif scheme in STORAGE_SCHEMES:
        return "storage"

    return "file_system"
