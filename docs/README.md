# 🎬 Multi-Agent Content Pipeline  

A modular, multi-agent pipeline for extracting, enriching, and publishing audio-based content from platforms like YouTube. Designed for transparency, auditability, and enterprise-grade scalability.

---

## 🚀 Overview

This project orchestrates audio extraction, transcription, metadata enrichment, and publishing workflows across multiple platforms. It supports CLI invocation, schema enforcement, and future agent-based routing via an MCP server.

For system internals, see [docs/architecture.md](docs/architecture.md).  
For folder layout, see [docs/project_structure.md](docs/project_structure.md).  
For testing strategy and coverage, see [docs/test_strategy.md](docs/test_strategy.md).

---

## 📦 Key Features

- Modular extractors for YouTube, stream services, and local files
- CLI orchestration with structured logging and error handling
- Unified metadata schema with validation and test coverage
- Semantic versioning and milestone-based release discipline

---

## 📈 Milestone Status

### ✅ Completed
Initial CLI-based YouTube audio extractor with MP3 conversion  
Local video support for MP4 ingestion  
Retry logic and logging hardening with yt-dlp integration  
Post-merge cleanup and changelog recovery  
Metadata extraction and schema enforcement  
Architecture overhaul and multi-agent readiness

### 🔨 In Progress
- Finalizing `breaking/architecture-overhaul`
- Scaffolding documentation suite
- Preparing release `v0.4.0`

### 🧭 Upcoming

- 🎙️ Transcribe audio to text using platform-agnostic modules  
- 🤖 Summarize transcripts with LLMs to generate highlights, tags, and metadata  
- 📝 Format outputs for publishing (blogs, threads, chapters, SEO)  
- 📦 Archive and index enriched content in a searchable store  
- 🧠 Integrate MCP server for agent routing, retries, and tagging  
- 🖥️ Build a GUI for reviewing and editing metadata  
- 📊 Add real-time observability: logging, tracing, and metrics

---

## 📄 License

This project is licensed under  
**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**

You may:
- Share and adapt the material with attribution  
- Not use it for commercial purposes  
- Not use it for training machine learning models (including LLMs) without explicit permission  

See [LICENSE.md](../LICENSE.md) for full legal terms.  
Full license text: [https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)


