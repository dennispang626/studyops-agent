# 5-Minute Demo Video Script

## 0:00 - 0:30 Problem

Professional certifications can improve career mobility, but studying for them
is messy. Learners have official guides, documentation, courses, personal notes,
practice questions, and risky exam-dump sites all mixed together. StudyOps Agent
solves this by creating one safe study station for certification prep.

## 0:30 - 1:00 Solution

StudyOps Agent helps a learner prepare for AWS Certified AI Practitioner AIF-C01
and AWS Certified Cloud Practitioner CLF-C02. It curates trusted sources,
creates Obsidian-style notes, retrieves context, builds a study plan, generates
original exam-style practice, and tracks weak topics for retry.

## 1:00 - 1:45 Architecture

Show the Agents page.

The system uses a multi-agent ADK design:

- Source Curator Agent
- Trust and Noise Filter Agent
- Knowledge Architect Agent
- Study Planner Agent
- Practice Coach Agent
- Examiner and Remediation Agent

Mention the stack: static Vercel UI, FastAPI backend bridge, optional MCP
tools, OKF-style Obsidian vault, Chroma-compatible retrieval, SQLite learner
memory, and ADK agent orchestration.

## 1:45 - 2:30 Setup and Sources

Show the Setup page.

Select AWS Certified AI Practitioner. Show the learner goal and weekly hours.
Classify an official AWS source. Explain that StudyOps blocks exam dumps,
prompt-injection phrases, and unsafe source text. Show file-note ingestion as
the path for learner-owned notes.

Mention that the public Vercel UI is connected to a local backend bridge for
the demo, so private vault files, API keys, and SQLite memory stay on the
learner's laptop.

## 2:30 - 3:20 Study Page

Show the Study page.

Click through the domain plan. Explain how StudyOps turns domains into active
study guidance, checklist items, notes, and RAG-style retrieval. Show a query
against the notebook and point to cleaned citations, relevance scores, and
study bullets returned by the backend `/api/studyops/rag-context` endpoint.

## 3:20 - 4:20 Practice and Memory

Show the Practice page.

Answer one question correctly and one incorrectly. Submit. Show that feedback
explains the correct answer and why each wrong option is wrong. Show weak
topics, retry queue, attempts, and confidence score.

Say clearly: these are generated exam-style practice questions, not official
questions or exam dumps.

## 4:20 - 4:50 Course Concepts

Summarize course concepts demonstrated:

- ADK multi-agent system
- MCP tool surface
- RAG over Obsidian notes
- Context engineering and citations
- SQLite memory and retry queue
- Safety guardrails
- Deployable web UI

## 4:50 - 5:00 Close

StudyOps is a focused MVP for career upskilling. It helps learners turn noisy
certification prep into a safe, structured, measurable study loop.
