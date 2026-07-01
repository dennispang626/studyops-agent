# StudyOps MCP

The MCP-facing server module is implemented at `app/mcp_server.py`.

Tools exposed:

- `search_certification_sources`
- `classify_certification_source`
- `fetch_and_clean_source`
- `seed_studyops_source_map`
- `ingest_certification_source`
- `ingest_uploaded_file`
- `write_obsidian_note`
- `list_obsidian_notes`
- `search_obsidian_notes`
- `rebuild_chroma_index`
- `generate_rag_context`
- `create_study_plan`
- `generate_practice_quiz`
- `submit_practice_answers`
- `run_studyops_workflow_tool`
- `record_practice_attempt`
- `get_learning_memory`
- `get_retry_queue`

Phase 5 adds the source-to-quiz workflow tools. Chroma is used when installed;
otherwise the local JSON fallback index is used for deterministic tests and
demos.

Run later, after dependencies are installed:

```bash
python -m app.mcp_server
```
