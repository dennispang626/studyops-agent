# Phase 8 - Deployment Packaging

Phase 8 prepares StudyOps Agent for GitHub, Vercel, and later backend
deployment. It does not perform a live deployment.

## What Was Added

- GitHub Actions CI workflow in `.github/workflows/ci.yml`.
- Deployment guide in `DEPLOYMENT.md`.
- Frontend package metadata in `frontend/package.json`.
- Dockerfile adjusted so builds do not require a missing `uv.lock`.
- Python package metadata adjusted so only `app` is treated as a Python package.
- Packaging contract tests.

## Current Deployment Recommendation

Frontend:

- Deploy `frontend/` as a static Vercel project.

Backend:

- Use Cloud Run when backend deployment is needed.
- Keep backend optional for the capstone demo because the frontend supports
  browser-local mode.

## Access Still Needed Later

- GitHub repository access if you want me to push the repo.
- Vercel access if you want me to deploy the frontend.
- Google Cloud project and credentials if you want me to deploy the backend.

## Deployment Gate

Before deployment:

- Unit tests should pass.
- JavaScript syntax check should pass.
- No `.env`, local DB, generated Chroma index, or secrets should be committed.
- `agents-cli eval generate` and `agents-cli eval grade` should be run once ADK
  dependencies and model credentials are available.
