# StudyOps Agent: Certification Study Coach for Career Upskilling

## Subtitle

An ADK multi-agent study station that turns trusted certification sources into
Obsidian notes, RAG context, exam-style practice, and weak-topic remediation.

## Track

Agents for Good

## Problem

Professional certifications can help learners prove skills, prepare for new
roles, and build career mobility. The difficult part is not motivation; it is
the scattered learning workflow. Certification information lives across
official pages, documentation, courses, personal notes, and practice resources.
Some material is outdated, some is too expensive, and unsafe exam-dump content
can harm both learning quality and ethics.

StudyOps Agent focuses on that gap. It gives an individual learner a single
study station for AWS Certified AI Practitioner AIF-C01, with AWS Certified
Cloud Practitioner CLF-C02 as a second supported path. The goal is not to
guarantee a pass or reproduce official questions. The goal is to help learners
study from trusted sources, practice safely, and improve weak topics over time.

## Solution

StudyOps Agent is a local-first certification coach. A learner selects a
certification, defines a goal, ingests trusted resources or their own study
files, reviews a domain-based plan, practices generated exam-style questions,
and receives feedback that explains why each option is correct or wrong.

The system stores knowledge in an Obsidian-compatible Markdown vault, indexes
notes for RAG retrieval, and records quiz attempts, weak topics, confidence
score, and retry items in SQLite. This makes the learning loop visible and
repeatable:

1. Curate sources.
2. Filter unsafe or noisy content.
3. Build structured notes.
4. Retrieve cited context.
5. Generate original practice questions.
6. Score answers.
7. Retry weak areas.

## Why Agents

A chatbot can answer one question at a time, but it does not naturally manage a
study workflow. StudyOps uses agents because the task has distinct specialist
responsibilities: source curation, safety filtering, knowledge-base creation,
planning, practice generation, and remediation. The multi-agent architecture
makes each responsibility explicit, easier to test, and easier to explain in a
portfolio.

## Architecture

The MVP uses Google ADK for the agent layer, FastAPI for backend routes, a
static Vercel-ready frontend, an optional MCP server, Obsidian Markdown notes,
Chroma-compatible retrieval, and SQLite memory.

The root orchestrator coordinates six specialist agents:

- Source Curator Agent: selects supported certifications and official source candidates.
- Trust and Noise Filter Agent: blocks exam-dump language, prompt injection, secrets, and unsafe sources.
- Knowledge Architect Agent: writes Obsidian notes and rebuilds the RAG index.
- Study Planner Agent: creates domain-based weekly plans.
- Practice Coach Agent: generates original exam-style practice questions.
- Examiner and Remediation Agent: scores answers, records weak topics, and manages retry items.

The frontend is organized into four pages:

- Agents: workflow trace and session metrics.
- Setup: certification, learner goal, sources, and uploads.
- Study: domain plan, active study guidance, notes, and retrieval.
- Practice: quiz, per-option feedback, confidence, attempts, weak topics, and retry queue.

## Course Concepts Demonstrated

StudyOps demonstrates at least three required course concepts:

- ADK agent / multi-agent system: implemented as a root orchestrator with six specialist sub-agents.
- MCP server: exposes StudyOps tools for source handling, ingestion, RAG, planning, quiz, and memory.
- Agent skills / workflow skills: the workflow packages repeatable source-to-quiz behavior into callable tools.
- RAG: retrieves context from Obsidian Markdown notes using a Chroma-compatible index with a deterministic fallback.
- Security features: blocks exam dumps, redacts secrets and PII, detects prompt-injection phrases, and labels generated questions clearly.
- Deployability: Vercel-ready frontend and FastAPI routes for backend integration.

## Implementation Highlights

The MVP is deliberately focused. The browser demo works without cloud keys by
using local deterministic data and browser storage, while the backend exposes
matching `/api/studyops/*` routes for deployment later.

The practice questions are original and scenario-style. They are not copied
from official AWS assessments, and the product labels them: "Generated exam-style practice, not official questions." Each question includes a correct
answer and option-level explanations so learners can understand mistakes
instead of only seeing a score.

The safety layer is central to the design. StudyOps refuses leaked questions and
exam dumps, avoids guaranteed-pass claims, and treats retrieved web or uploaded
content as untrusted until checked.

## User Value

StudyOps helps learners study in a more structured way:

- It reduces noise by separating trusted sources from unsafe material.
- It turns scattered content into a personal knowledge base.
- It supports active recall with practice questions and explanations.
- It records weak topics so learners can improve instead of repeating the same mistakes.
- It gives a portfolio-friendly example of agentic engineering, RAG, MCP, memory, and safety.

## Limitations and Next Steps

The current capstone version is an MVP. It supports AWS AI Practitioner and AWS
Cloud Practitioner first. Live search API integration, production deployment,
LLM-assisted question generation with strict evaluation, and richer uploaded PDF
parsing are natural next steps.

The project is built to grow, but the capstone submission prioritizes a crisp,
demoable workflow over an oversized system.
