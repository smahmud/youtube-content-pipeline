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

---

## 3. Folder Layout

All tests are located in the `tests/` directory, organized by module:

---

## 🧪 `tests/` — Test Suite

This folder contains unit and integration tests for core pipeline components, organized by functionality and platform.

```text
tests/
├── __init__.py
├── test_cli.py               # Validates CLI entry point and orchestration logic
├── test_integration.py       # Full pipeline integration test
├── assets/
│   └── local/
│       ├── __init__.py
│       ├── test_file_audio.py       # Tests local audio ingestion and conversion
│       └── test_metadata_utils.py   # Tests metadata extraction from local files
├── outputs/
│   └── youtube/
│       ├── __init__.py
│       └── test_extractor.py        # Tests YouTube extractor logic and metadata normalization
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

Execution Examples
Run the full test suite:
```bash
pytest tests/
```
Run all tests in a specific file:
```bash
pytest tests/test_cli.py
```
Run a specific test function by name:
```bash
pytest tests/test_cli.py::test_flag_parsing
```

>**Note:**
>All tests use pytest with unittest.mock for isolation
>Integration tests reflect real CLI usage and agent orchestration
>Coverage for streamservice extractors (e.g. Vimeo, TikTok) will be added after v1.0.0

Code

### 5. Mocking and Isolation

External dependencies (e.g. YouTube downloads, file I/O) are mocked using `unittest.mock` to ensure deterministic behavior and fast execution.

---

### 6. Milestone Coverage — v0.4.0

- YouTube extractor logic  
- Local file ingestion  
- Metadata schema enforcement  
- CLI orchestration and flag parsing

---

### 7. Future Plans

- Add transcription module tests in `v0.5.0`  
- Integrate coverage reporting and CI hooks
