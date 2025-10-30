# System Architecture Overview

This document outlines the high-level architecture of the YouTube Content Pipeline, designed for scalable, multi-agent audio and metadata extraction across platforms like YouTube and TikTok. It supports CLI orchestration, schema enforcement, and modular agent integration.

---

## 🧩 Core Components

### 1. Extractors
Platform-specific modules that handle audio and metadata extraction.

pipeline/extractors/
 ├── local/
 │   ├── extractor.py       # Local file-based extraction logic
 │   ├── transcriber.py
 │   └── metadata.py
 ├── youtube/
 │   ├── extractor.py # Unified entry point for YouTube extraction
 ├   ├── transcriber.py # Audio transcription logic 
 │   ├── metadata.py # Metadata parsing and enrichment 
 ├── streamservice/ 
 │   ├── extractor.py 
 │   ├── transcriber.py 
 │   └── metadata.py


Each extractor implements a shared interface (`BaseExtractor`) to ensure compatibility with CLI and agent orchestration.

---

### 2. CLI Orchestration

pipeline/cli.py

- Entry point for invoking extractors via command-line
- Supports flags like `--extract-audio`, `--extract-metadata`, `--platform youtube`
- Handles logging, error propagation, and output normalization

---

### 3. Schema Enforcement

pipeline/schema/metadata.py

- Defines the canonical metadata schema used across extractors
- Enforced via unit tests and integration validation
- Ensures consistent downstream consumption by agents or GUI

---

### 4. Configuration & Logging

pipeline/config/logging.py

- Centralized logging setup for CLI, extractors, and tests
- Supports structured logs and configurable verbosity

---

### 5. Utilities

pipeline/utils/retry.py

- Generic retry logic for transient failures (e.g., network, API)
- Used across extractors and CLI

---

## 6. Multi-Agent Protocol (Planned)

The pipeline will integrate with an MCP server to support agent-based orchestration:

- Agents will invoke extractors via CLI or direct module calls
- Metadata and audio outputs will be tagged and routed via shared schema
- Future support for GUI enrichment and real-time observability

---

## 7. Observability & Testing

- Integration tests validate CLI behavior and extractor output
- Logging is unified across all components
- Future plans include tracing and metrics for agent workflows

---

## 8 Test Coverage

- Unit tests validate extractor logic, schema compliance, and CLI flag behavior
- Integration tests simulate real input scenarios across platforms and verify output normalization
- Test scaffolds mirror actual CLI invocation and project structure
- Future plans include protocol-level agent tests and error scenario validation

---

## 📦 Versioning Discipline

- Semantic versioning is enforced:
  - `v0.2.x`: CLI integration and logging hardening
  - `v0.3.x`: Metadata extraction and schema enforcement
  - `v0.4.x`: Architecture overhaul and multi-agent readiness

---

## 📁 Folder Summary
docs/                         # Architecture, CLI reference, schema, and project structure

pipeline/ 
├── extractors/ # Platform-specific logic 
├── schema/ # Shared data contracts 
├── config/ # Logging and runtime setup 
├── utils/ # Reusable helpers 
├── cli.py # CLI entry point

tests/                        # Unit and integration tests

changelog.md                 # Version history and release notes
Makefile                     # Task automation and developer shortcuts
pytest.ini                   # Pytest configuration
README.md                    # Executive summary and onboarding
requirements.txt             # Runtime dependencies
requirements-dev.txt         # Dev/test dependencies
requirements.lock.test       # Locked test environment
setup.py                     # Packaging and distribution metadata
---

## 🧭 Future Directions

- 🎙️ Transcribe audio to text using platform-agnostic `transcriber.py` modules  
- 🤖 Summarize transcripts with LLMs to generate structured highlights, tags, and semantic metadata  
- 📝 Format enriched outputs for publishing: blog drafts, tweet threads, chapters, and SEO tags across platforms like Twitter, Bluesky, Instagram, and Facebook  
- 📦 Archive and index all enriched content into a searchable store  
- 🧠 Integrate MCP server for agent orchestration, routing, retries, and tagging  
- 🖥️ Build a GUI for reviewing and editing enriched metadata before publishing  
- 📊 Add real-time observability: structured logging, tracing, and metrics across pipeline stages  


