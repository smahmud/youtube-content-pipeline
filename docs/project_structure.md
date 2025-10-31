# 🧱 Project Structure

This document outlines the folder and file layout of the Multi-Agent Content Pipeline. It reflects modularity, semantic discipline, and milestone-aligned growth across extractors, enrichment, publishing, and orchestration.

---

## 📂 `pipeline/` — Core Modules

This folder contains the core logic for extraction, enrichment, publishing, and orchestration. Each submodule is milestone-aligned and semantically scoped.

```bash
pipeline/
├── extractors/              # Platform-specific logic
│   ├── youtube/             # YouTube audio and metadata extraction
│   ├── streamservice/       # Generic streaming service scaffold
│   ├── local/               # Local file-based extraction
├── transcriber/             # Audio-to-text transcription modules
├── summarizer/              # LLM-based transcript summarization
├── content_generator/       # Output formatting for publishing
├── sentiment_analyzer/      # Tone and emotion classification
├── enrichment/              # Legacy placeholder (may be deprecated or merged)
├── publishing/              # Legacy placeholder (may be deprecated or merged)
├── archive/                 # Indexing and storage (planned)
├── routing/                 # MCP agent coordination and dispatch (planned)
├── schema/                  # Shared metadata schema definitions
├── config/                  # Logging and runtime setup
├── utils/                   # Reusable helpers (e.g., retry logic)
├── cli.py                   # CLI entry point for orchestrating extractors

---

## 📦 Root-Level Files

This section describes the purpose of each file located at the root of the repository.

| File                     | Purpose                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| `README.md`              | Executive summary, onboarding, and milestone status                     |
| `changelog.md`           | Semantic version history and release notes                              |
| `Makefile`               | Developer shortcuts and task automation                                 |
| `pytest.ini`             | Pytest configuration for test discovery and behavior                    |
| `requirements.txt`       | Runtime dependencies for production use                                 |
| `requirements-dev.txt`   | Development and testing dependencies                                    |
| `requirements.lock.test` | Locked test environment for reproducibility                             |
| `setup.py`               | Packaging and distribution metadata                                     |
| `cli.py`                 | CLI entry point for orchestrating extractors and pipeline modules       |
| `logging_config.py`      | Centralized logging setup for structured observability                  |
| `metadata_schema.py`     | Canonical metadata schema used across extractors and enrichment modules |

---

## 🧪 `tests/` — Validation Suite

- **Unit tests** for individual extractors, schema validators, and utility functions  
- **Integration tests** for CLI workflows and multi-agent orchestration  
- **Schema compliance** checks to validate output structure and field integrity  
- **Error handling** tests to ensure graceful failure and retry logic  
- Mirrors actual CLI invocation and extractor usage

---

## 📘 `docs/` — Documentation Suite

This folder contains all architectural, operational, and milestone-related documentation. Each file is scoped to a specific concern to maintain clarity and avoid duplication.

| File                  | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `architecture.md`     | High-level system design, agent orchestration, and milestone alignment  |
| `project_structure.md`| Explains folder layout and rationale (this file)                        |
| `metadata_schema.md`  | Canonical schema contract and field definitions                         |
| `test_strategy.md`    | How unit and integration tests are structured and validated             |
