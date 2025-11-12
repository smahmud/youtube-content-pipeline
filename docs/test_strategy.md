# 🧪 Test Strategy

This document outlines the testing approach for the Content Pipeline project, focusing on reliability, modularity, and milestone alignment.

---

## 1. Purpose and Scope

The testing strategy ensures that all core components — extractors, CLI orchestration, and metadata schema — behave predictably across platforms and inputs. It covers unit tests, integration tests, and schema validation.

---

## 2. Test Types

- **Unit Tests**  
  Validate isolated functions and classes, especially in extractors and schema utilities.

- **Integration Tests**  
  Simulate end-to-end flows across CLI, extractors, and metadata normalization.

- **Schema Validation**  
  Enforce field-level correctness using `pipeline/schema/metadata.py`.

- **CLI Invocation Tests**  
  Ensure CLI commands execute correctly with expected flags and outputs.

- **Transcript Normalization Tests**  
  Validate `TranscriptV1` schema compliance and adapter behavior across transcriber outputs.

---

## 3. Folder Layout

All tests are located in the `tests/` directory, organized by module:

---

## 🧪 `tests/` — Test Suite

This folder contains unit and integration tests for core pipeline components, organized by functionality and platform.

```text
tests/
├── assets/
│   ├── sample_audio.mp3
│   ├── sample_transcript_v1.json
│   ├── sample_transcript.txt
│   ├── sample_video_metadata.json
│   ├── sample_video.mp4
│   └── sample_whisper_raw_output.json
├── output/
├── cli/
│   ├── test_extract_cli.py
│   └── test_transcribe_cli.py
├── integration/
│   ├── test_extract_pipeline_flow.py
│   └── test_transcribe_pipeline_flow.py
├── pipeline/
│   ├── extractors/
│   │   ├── local/
│   │   │   └── test_file_audio.py
│   │   ├── youtube/
│   │   │   └── test_extractor.py
│   │   └── schema/
│   │       └── test_metadata.py
│   └── transcribers/
│       ├── adapters/
│       │   └── test_whisper_adapter.py
│       ├── schemas/
│       │   └── test_transcript_v1.py
│       ├── test_normalize.py
│       ├── test_persistence.py
│       ├── test_transcriber.py
│       └── test_validate.py

```

---

### 4. Execution

Tests are executed using `pytest`, with support for selective execution via markers defined in `pytest.ini`.

#### Marker Usage

To run only integration tests:

```bash
pytest -m "integration"
```
To exclude integration tests and run only unit tests:

```bash
pytest -m "not integration"
```

To run only slow tests:

```bash
pytest -m "slow"
```

To exclude slow tests:

```bash
pytest -m "not slow"
```

Execution Examples
Run the full test suite:
```bash
pytest tests/
```
Run all tests in a specific file:
```bash
pytest tests/cli/test_extract_cli.py
```
Run a specific test function by name:
```bash
pytest tests/integration/test_extract_pipeline_flow.py::test_extract_audio_from_youtube_integration
```

>**Note:**
>All tests use pytest with unittest.mock for isolation
>Integration tests reflect real CLI usage and agent orchestration

---

### 5. Mocking and Isolation

External dependencies are mocked using `unittest.mock` to ensure deterministic behavior and fast execution.

- **YouTube downloads** and file I/O are mocked to avoid network and disk dependencies  
- **Whisper transcription** is mocked in transcriber adapter tests to isolate normalization and persistence logic  
- **Metadata builders** are tested with placeholder inputs to avoid real source classification

---

### 6. Milestone Coverage — v0.5.0

- Transcriber adapter behavior using OpenAI Whisper  
- Transcript normalization with `TranscriptV1` schema  
- File-system persistence for transcript and metadata artifacts  
- CLI subcommand routing via `click` group (`extract`, `transcribe`)  
- Source classification via `dispatch.classify_source()`  
- Metadata schema validation for structural source types (`streaming`, `storage`, `file_system`)

---

### 7. Future Plans

- Add test coverage for streaming transcription and confidence scoring  
- Validate transcript enrichment and segment filtering logic  
- Scaffold CLI test coverage for modular subcommands (`extract`, `transcribe`, etc.)  
- Introduce extractor interface compliance tests for future platforms (TikTok, Vimeo)  
- Integrate coverage reporting and CI hooks for milestone tracking

