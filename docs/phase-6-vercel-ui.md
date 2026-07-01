# Phase 6 - Vercel UI

Phase 6 adds the capstone-facing web experience for StudyOps Agent.

## What Was Built

- Static Vercel UI in `frontend/`, organized into focused app pages.
- Browser-local workflow mode for demos without credentials.
- Optional backend integration through `/api/studyops/workflow`.
- FastAPI StudyOps routes for workflow, study plan, quiz generation, and answer
  submission.
- Local learner memory in `localStorage`.

## Frontend Panels

- Agents page with six-step workflow trace and session metrics.
- Setup page for provider, certification, learner goal, source classification,
  and local file-note ingestion.
- Study page for domain planning, active study guidance, notebook review, and
  RAG-style local context retrieval over generated notes.
- Practice page for generated exam-style quiz, per-option answer explanations,
  confidence score, weak-topic memory, retry queue, and attempts.

## Backend Contract

The UI can call:

- `POST /api/studyops/workflow`
- `POST /api/studyops/study-plan`
- `POST /api/studyops/practice-quiz`
- `POST /api/studyops/practice-submit`

If no backend URL is configured, it uses the same data contract in local demo
mode.

## Deployment Note

Deploy the `frontend/` folder to Vercel as a static project. No login is needed
for the demo mode. When the backend is deployed later, configure the frontend
with the public FastAPI base URL.
