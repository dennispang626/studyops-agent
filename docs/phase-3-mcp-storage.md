# Phase 3 MCP and Storage Notes

Status: complete.

## What Was Built

Phase 3 adds the local foundations needed before live RAG and multi-agent
workflow work begins.

Implemented modules:

- `app/config.py`
- `app/security/source_trust.py`
- `app/storage/obsidian_vault.py`
- `app/storage/sqlite_store.py`
- `app/tools/studyops_tools.py`
- `app/mcp_server.py`

## Storage

### Obsidian Vault

`ObsidianVault` writes Markdown notes under `data/obsidian_vault`. Notes include
simple front matter and are safe against path traversal.

### SQLite Learner Memory

`SQLiteStudyStore` creates these tables:

- `learners`
- `quiz_attempts`
- `answers`
- `weak_topics`
- `retry_queue`
- `sources`

It can record a quiz attempt, update weak-topic memory, and create retry items
for missed topics.

## Safety

`classify_source` scores sources as official, trusted, unverified, or unknown.
It blocks exam-dump language and flags prompt-injection-like text. Redaction
helpers remove obvious secrets, email addresses, and phone numbers before text is
stored.

## Tools

`app/tools/studyops_tools.py` exposes plain Python functions that can be used by:

- ADK as agent tools
- the optional MCP server
- future FastAPI endpoints
- unit tests

## MCP

`app/mcp_server.py` uses `FastMCP` when the optional `mcp[cli]` dependency is
installed. The dependency is listed in `pyproject.toml`, but it was not installed
in this phase because the current Windows environment already showed long-path
issues during Phase 2 dependency setup.

## Phase 4 Update

The following items were built in Phase 4:

- live web fetching
- uploaded file parsing
- Chroma indexing
- semantic RAG context generation

Still not built yet:

- generated quiz content
- LLM-based note synthesis
- live search API provider integration

