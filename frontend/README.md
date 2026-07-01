# StudyOps Frontend

This folder contains the Vercel-ready static web UI for StudyOps Agent.

Open `index.html` directly for the local demo, or deploy this folder as a
static Vercel project.

## Runtime Modes

- Browser-local demo mode: runs without credentials or backend access.
- Backend mode: set `window.STUDYOPS_API_BASE_URL` or `localStorage.studyops_api_base`
  to a FastAPI base URL that exposes `/api/studyops/workflow`.

## Implemented Panels

- Agents page with workflow trace and quick session metrics
- Setup page with provider, certification, learner settings, source
  classification, and file-note ingestion
- Study page with domain plan, active study guidance, Obsidian-style notes, and
  RAG-style local context retrieval
- Practice page with generated exam-style quiz, detailed per-option feedback,
  confidence score, weak-topic memory, retry queue, and attempts

Generated questions are labeled as exam-style practice, not official questions.
