# Metadata Schema Specification

This document defines the canonical metadata structure used across all extractors in the pipeline. It ensures consistency, auditability, and extensibility for downstream agents and enrichment workflows.

---

## 🧱 Base Metadata Fields

These fields are required across all sources (YouTube, local files, etc):

| Field           | Type                                | Description |
|----------------|-------------------------------------|-------------|
| `title`         | `str`                               | Human-readable title of the video |
| `duration`      | `Optional[int]`                     | Duration in seconds (if available) |
| `author`        | `Optional[str]`                     | Creator or uploader name |
| `source_type`   | `Literal["youtube_url", "local_file"]` | Indicates origin of the metadata |
| `source_path`   | `Optional[str]`                     | Absolute path to local file (if applicable) |
| `source_url`    | `Optional[str]`                     | Original URL of the video (if applicable) |
| `metadata_status` | `Literal["complete", "incomplete"]` | Indicates whether metadata is fully enriched |
| `service_metadata` | `dict`                           | Optional service-specific fields (see below) |

---

## 🔍 `source_type` Values

| Value         | Meaning |
|---------------|---------|
| `"youtube_url"` | Metadata extracted from a YouTube video URL |
| `"local_file"`  | Metadata generated from a local video file |

---

## 🧩 `service_metadata` Extensions

This field contains optional, service-specific metadata. It is empty for local files and populated when available from streaming services.

### Example: YouTube

```json
"service_metadata": {
  "view_count": 12345,
  "channel_id": "UCabc123",
  "like_count": 678
}
