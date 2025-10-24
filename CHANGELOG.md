# Changelog

All notable changes to this project will be documented in this file.

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
