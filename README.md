# StudyOps Agent

StudyOps Agent is an AI certification study coach for accessible career
upskilling. The capstone MVP helps learners prepare for AWS certifications by
curating trusted sources, building an Obsidian-friendly knowledge base,
generating grounded practice questions, tracking weak topics, and re-asking
missed concepts until the learner improves.

This project was scaffolded with `agents-cli` and Google ADK as a local-first
prototype. The web UI can run as a static Vercel demo now; cloud deployment
support will be added after the MVP is verified.

## Capstone Track

Kaggle AI Agents: Intensive Vibe Coding Capstone Project

Track: Agents for Good

## MVP Certifications

- Primary demo: AWS Certified AI Practitioner AIF-C01
- Secondary option: AWS Certified Cloud Practitioner CLF-C02

## Architecture

```text
Vercel Next.js UI
  -> FastAPI Agent Gateway
    -> ADK Root Agent: StudyOps Orchestrator
      -> Source Curator Agent
      -> Trust and Noise Filter Agent
      -> Knowledge Architect Agent
      -> Study Planner Agent
      -> Practice Coach Agent
      -> Examiner and Remediation Agent

Storage:
  data/obsidian_vault/ -> human-readable Markdown knowledge base
  data/chroma/ -> local vector index
  data/sqlite/ -> learner progress and retry queue
```

## Course Concepts Demonstrated

- ADK agent / multi-agent system
- MCP tools
- RAG over an Obsidian Markdown vault
- Transformer embeddings through the vector index
- LangChain-style document loading, splitting, and retrieval
- Context engineering with source grounding and citation rules
- Security guardrails for exam dumps, prompt injection, secrets, and PII
- Evaluation-driven development
- Deployable web UI

## Project Structure

```text
studyops-agent/
  app/                    # ADK agent and FastAPI backend
    agent.py              # ADK root agent entrypoint
    agents/               # ADK multi-agent factories
    fast_api_app.py       # Local-first FastAPI entrypoint
    mcp_server.py         # Optional MCP server for StudyOps tools
    app_utils/            # Generated telemetry and typing helpers
    knowledge/            # Certification catalog and blueprints
    workflows/            # Deterministic source-to-quiz workflow
    ingestion/            # Web/file ingestion and note generation pipeline
    rag/                  # Chunking and Chroma-compatible retrieval
    security/             # Source trust, redaction, and safety helpers
    storage/              # Obsidian and SQLite foundations
    tools/                # Python tool functions shared by ADK and MCP
  data/
    obsidian_vault/       # Markdown notes for RAG and human study
    chroma/               # Chroma or fallback JSON index
    sqlite/               # Local progress DB, generated later
  docs/                   # Architecture and implementation notes
  frontend/               # Static Vercel UI
    index.html            # Study cockpit first screen
    styles.css            # Responsive app styling
    app.js                # Browser-local workflow and backend contract client
    vercel.json           # Static Vercel routing
  submission/             # Kaggle writeup, video script, and demo checklist
  .github/workflows/      # CI checks for GitHub
  mcp/                    # MCP tool server placeholder, built in Phase 3
  tests/
    unit/                 # Deterministic code tests
    integration/          # Server and agent integration tests
    eval/                 # Agent behavior evals
  AGENTS.md               # Codex/agent development guidance
  agents-cli-manifest.yaml
  pyproject.toml
```

## Local Setup

1. Install `uv`.
2. Install `agents-cli`.
3. Copy `.env.example` to `.env` and fill in local values.
4. Install dependencies:

```bash
agents-cli install
```

5. Run the local playground:

```bash
agents-cli playground
```

In this workspace, use the parent wrapper while the global CLI is not on PATH:

```powershell
..\agents-cli-local.cmd info
```

## Frontend Demo

Open the static UI directly:

```text
frontend/index.html
```

The UI runs in browser-local demo mode by default. To connect it to a deployed
backend later, set `window.STUDYOPS_API_BASE_URL` or
`localStorage.studyops_api_base` to the FastAPI base URL.

## Environment

The project supports either Google AI Studio API-key mode for local prototyping
or Vertex AI mode later.

Required later for model calls:

- `GOOGLE_API_KEY` for local AI Studio mode, or
- `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and Vertex auth for cloud mode

No keys should ever be committed.

## Current Phase

Phase 9 GitHub and Vercel handoff is complete:

- ADK project scaffold exists.
- FastAPI backend entrypoint exists.
- Local-first environment placeholders exist.
- Storage and frontend directories are prepared.
- SQLite learner memory foundation exists.
- Obsidian Markdown vault foundation exists.
- Source trust and redaction helpers exist.
- ADK root agent now exposes the Phase 3 tool functions.
- Optional MCP server wrapper exists.
- File and source ingestion foundation exists.
- Obsidian note generation pipeline exists.
- Chroma-compatible RAG index with JSON fallback exists.
- Cited retrieval context tool exists.
- Certification catalog and blueprint helpers exist.
- Deterministic source-to-quiz workflow exists.
- ADK root orchestrator has six specialist sub-agents.
- Workflow tools are exposed through ADK and MCP.
- Generated practice questions are labeled as exam-style practice, not official
  questions.
- FastAPI exposes StudyOps workflow endpoints for the UI.
- Static Vercel frontend exists.
- Browser-local demo mode exists.
- UI supports certification selection, source classification, file-note
  ingestion, notebook search, study plan, quiz scoring, retry queue, and agent
  trace.
- StudyOps-specific eval datasets exist.
- Custom eval metrics for response quality, safety, and trace completeness exist.
- Kaggle writeup draft exists.
- Five-minute video script exists.
- Demo checklist and architecture submission notes exist.
- GitHub Actions CI workflow exists.
- Deployment guide exists.
- Frontend package metadata exists for Vercel/static checks.
- Dockerfile no longer requires a missing lockfile.
- `.dockerignore`, `.gitignore`, and `.env.example` are prepared.
- GitHub and Vercel handoff guide exists.
- Repeatable preflight script exists.
- Print-only release command plan exists.
- Phase 9 handoff asset tests exist.

The next live publishing step needs explicit approval plus GitHub and Vercel
access. Backend deployment also needs Google Cloud access.
