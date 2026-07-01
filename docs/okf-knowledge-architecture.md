# OKF-Style Knowledge Architecture

StudyOps now treats the Obsidian vault as an agent-maintained, OKF-style
Markdown wiki. Raw sources stay separate from compiled study knowledge.

## Pipeline

```text
Raw uploads / URLs / PDFs
  -> extracted source text
  -> OKF-style Obsidian Markdown wiki
  -> Chroma vector index
  -> RAG retrieval
  -> quiz/study/remediation agents
```

## Vault Layout

```text
data/obsidian_vault/
  index.md
  certificates/
    aws-ai-practitioner/
      index.md
      exam-blueprint.md
      study-plan.md
    aws-cloud-practitioner/
      index.md
      exam-blueprint.md
      study-plan.md
  concepts/
    foundation-models.md
    responsible-ai.md
    iam-for-ai-security.md
  sources/
    aws-official-ai-practitioner.md
    uploaded-pdf-001.md
  quizzes/
    weak-topics.md
```

## Note Contract

Every generated note uses portable YAML front matter:

```yaml
---
type: concept
title: Foundation Models
description: Study concept for AIF-C01.
tags: [concept, aws-ai-practitioner, foundation-models]
certification: AIF-C01
provider: AWS
source_url:
source_ids: []
review_status: agent_drafted
format: okf-style-markdown
format_version: 0.1
created: 2026-07-02T00:00:00+00:00
updated: 2026-07-02T00:00:00+00:00
---
```

## Storage Responsibilities

- Obsidian Markdown: human-readable long-term study memory.
- Chroma: semantic retrieval over curated notes.
- SQLite: learner memory, attempts, weak topics, retry queue, and source audit.

## Agent Responsibilities

- Source Curator Agent: finds or accepts candidate URLs/files.
- Trust and Noise Filter Agent: blocks exam dumps, prompt injection, and secrets.
- Knowledge Architect Agent: compiles source text into linked Markdown notes.
- RAG Indexer: chunks OKF notes and refreshes Chroma.
- Study Planner Agent: writes the learner study plan into the certificate wiki.
- Practice Coach Agent: generates cited exam-style practice from retrieved notes.
- Examiner and Remediation Agent: records scores and weak-topic memory in SQLite.

## Browser and Backend Modes

The Vercel frontend can still run in browser-local demo mode. When a backend URL
is configured, Setup intake calls:

- `POST /api/studyops/ingest-url`
- `POST /api/studyops/ingest-file`

Those routes write OKF-style Obsidian notes and rebuild the RAG index.
