# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2025-10-28

### Added
- `extract_metadata()` implementation for YouTube extractor to return structured metadata from video source
- Metadata schema definition in `pipeline/schema/metadata.py` to enforce consistent output structure
- Unit tests for metadata extraction and schema compliance

### Changed
- Refactored YouTube extractor to support both audio and metadata extraction via unified interface
- Updated CLI to support `--metadata-url` flag and dispatch accordingly
- Expanded test coverage to validate metadata output and CLI integration

## [0.2.2] - 2025-10-27

### Added
- Integration tests to validate CLI behavior and extractor output across real input scenarios
- Logging configuration scaffold to unify log formatting and control across pipeline components

### Changed
- Hardened post-merge pipeline by centralizing logging setup in `pipeline/config/logging.py`
- Enforced consistent logging usage across CLI, extractors, and tests
- Improved error handling and retry logic in CLI and extractor modules
- Refactored test scaffolds to match actual CLI invocation and project structure

## [0.2.1] - 2025-10-25
### Added
- Retry logic with exponential backoff for audio downloads
- Logging for successful and failed operations in CLI and extractor

### Changed
- Replaced `pytubefix`, `pydub`, and `ffmpeg-python` with `yt-dlp` for more robust YouTube audio extraction
- Normalized `.mp3` output handling to prevent double extensions
- Updated `setup.py` to set version to `0.2.1` and include `yt_dlp` in `install_requires`

### Notes
- `yt-dlp` and `moviepy` require the `ffmpeg` binary to be installed and available in your system PATH
- You can download `ffmpeg` from https://ffmpeg.org/download.html

## [0.2.0] - 2025-10-24
### Added
- Support for local MP4 video files in CLI
- Unified input handling for remote and local sources
- Introduced `moviepy` for audio extraction and MP3 conversion

### Changed
- Updated `setup.py` to include `moviepy` in `install_requires`
- Set version to `0.2.0` in `setup.py`

### Notes
- Replaced `pytube` with `pytubefix` for improved YouTube video handling

## [0.1.1] - 2025-10-22
### Fixed
- Corrected `setup.py` entry point and dependency issues

## [0.1.0] - 2025-10-20
### Added
- Initial CLI for extracting audio from YouTube URLs
- MP3 conversion using `pytubefix`
