# Phase 5 - Multi-Agent Workflow

Phase 5 turns the StudyOps foundations into a focused, demoable agent system.
The implementation keeps the core workflow deterministic so judges can run it
without external access, while the ADK root agent exposes the same capabilities
through specialist sub-agents.

## What Was Built

- `app/workflows/studyops_workflow.py` implements the source-to-quiz workflow.
- `app/agents/studyops_agents.py` defines the ADK root orchestrator and six
  specialist agents.
- `app/tools/studyops_tools.py` exposes the workflow as function tools.
- `app/mcp_server.py` registers the new workflow tools for MCP use.
- `tests/unit/test_phase5_workflow.py` verifies the local workflow.

## Agent Roles

1. Source Curator Agent
   - Selects supported certifications and official source candidates.
   - Seeds an Obsidian source-map note.

2. Trust and Noise Filter Agent
   - Classifies sources.
   - Blocks exam-dump language and treats retrieved text as untrusted data.

3. Knowledge Architect Agent
   - Writes Obsidian notes.
   - Rebuilds the Chroma-compatible RAG index.

4. Study Planner Agent
   - Converts exam domains and learner goals into a weekly plan.

5. Practice Coach Agent
   - Generates safe practice questions from blueprint and RAG context.
   - Labels questions as generated exam-style practice, not official questions.

6. Examiner and Remediation Agent
   - Scores answers.
   - Updates weak topics and retry queue in SQLite.

## Demo Workflow

`run_studyops_workflow_tool` produces a complete demo payload:

- source trust trace
- source-map Obsidian note
- RAG index rebuild result
- weekly study plan
- generated practice quiz
- learner memory snapshot

The workflow does not need live search, GitHub, Vercel, or Obsidian sync. It
uses local storage paths from the `STUDYOPS_*` environment variables.

## Course Concepts Demonstrated

- ADK multi-agent system
- MCP-compatible tool surface
- RAG over an Obsidian Markdown vault
- Context engineering with citations and source-map notes
- SQLite memory for weak topics and retry queue
- Security guardrails for exam dumps, prompt injection, secrets, and PII

## Current Limitations

- Practice questions are deterministic placeholders for the MVP demo. Later
  phases can replace the generator with LLM-assisted generation plus evals.
- Live search API integration remains behind the existing ingestion tools.
- The Vercel UI has not been built yet.

