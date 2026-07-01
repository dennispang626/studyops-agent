# Phase 4 RAG and Obsidian Pipeline Notes

Status: complete.

## What Was Built

Phase 4 turns the Phase 3 storage foundations into a usable knowledge pipeline.

Implemented modules:

- `app/ingestion/source_fetcher.py`
- `app/ingestion/file_loader.py`
- `app/ingestion/pipeline.py`
- `app/rag/chunking.py`
- `app/rag/index.py`

Updated modules:

- `app/tools/studyops_tools.py`
- `app/mcp_server.py`
- `app/agent.py`
- `pyproject.toml`

## Pipeline

```text
web source or uploaded file
  -> trust check / redaction / cleaning
  -> deterministic study-note body
  -> Obsidian Markdown note
  -> Markdown chunking
  -> Chroma-compatible index
  -> cited retrieval context
```

## Chroma Strategy

The project declares `chromadb` in `pyproject.toml`. `StudyOpsRagIndex` tries to
use Chroma when the package is installed. If Chroma is unavailable or fails at
runtime, the system writes a deterministic JSON fallback index to the configured
Chroma directory.

This is intentional for the capstone MVP:

- The interface is Chroma-compatible.
- Local tests do not require heavyweight dependency installation.
- The fallback index makes demo behavior deterministic.
- A later environment setup can install Chroma and use the same tool functions.

## New Tools

- `fetch_and_clean_source`
- `ingest_certification_source`
- `ingest_uploaded_file`
- `rebuild_chroma_index`
- `generate_rag_context`

## Current Limitations

- Live search API provider is still not wired; official curated source fallback
  remains available.
- PDF parsing is not enabled yet.
- Retrieval quality is lexical in fallback mode.
- LLM-based note synthesis and quiz generation begin in Phase 5.

