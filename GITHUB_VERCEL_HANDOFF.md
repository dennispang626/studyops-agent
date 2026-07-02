# StudyOps GitHub and Vercel Handoff

Phase 9 prepared StudyOps Agent for portfolio publishing, then published the
frontend for live UI tuning.

## Current State

- GitHub repository: https://github.com/dennispang626/studyops-agent
- Production frontend: https://studyops-agent.vercel.app
- Vercel project: https://vercel.com/dennis-heku/studyops-agent
- The backend is packaged for a later Cloud Run deployment.
- The production frontend can run in browser-local demo mode or connect to the
  local FastAPI bridge at `http://127.0.0.1:8000`.
- The local bridge writes to the private Obsidian vault, RAG index, and SQLite
  learner memory on the laptop.
- No Google Cloud credentials are required for the current capstone demo path.

## Preflight

Run the local preflight before every publish attempt:

```powershell
.\scripts\preflight.ps1
```

It checks:

- Python syntax for the workflow, tools, and FastAPI app.
- Frontend JavaScript syntax.
- Unit test suite.

## GitHub Publish Plan

The first public repo push has been completed. Reuse this flow for future
changes:

```powershell
git add .
git commit -m "Describe the UI or agent change"
git push
```

Before every push, re-check:

- `.env` is not committed.
- `data/sqlite/studyops.db` is not committed.
- generated Chroma index files are not committed.
- generated Obsidian vault notes are not committed unless intentionally curated.
- no API keys, passwords, private files, or real exam dump content are present.

## Vercel Frontend Plan

The Vercel project has been created under `dennis-heku/studyops-agent`.
For future frontend updates:

```powershell
npx vercel@latest deploy frontend --prod --yes --scope dennis-heku
```

The frontend works without a backend in browser-local demo mode. For the
stronger personal demo, start the local backend bridge and set the Setup page
API base URL to `http://127.0.0.1:8000`.

When a backend is deployed later, connect it with:

```js
localStorage.setItem("studyops_api_base", "https://your-backend.example.com");
```

Then refresh the Vercel page.

The current `frontend/vercel.json` provides clean URLs, a content-type safety
header, and a rewrite to `index.html` so deep links keep loading the app shell.

## Backend Deployment Gate

Recommended backend target: Cloud Run.

Access needed before backend deployment:

- Google Cloud project ID.
- Billing-enabled project.
- `gcloud` or `agents-cli` authentication.
- `GOOGLE_API_KEY` or Vertex AI environment variables.
- Deployed frontend URL for `ALLOW_ORIGINS`.

Do not deploy the backend until:

- preflight passes.
- capstone demo flow is verified.
- eval datasets are reviewed.
- secrets are stored in platform secret managers, not committed files.

## Public Links for Kaggle

For the Kaggle submission, prepare:

- Public GitHub repository URL or clearly documented public code package.
- Public Vercel frontend URL.
- Optional backend URL if deployed and login-free.
- YouTube demo video URL.
- Kaggle Writeup with media gallery, cover image, project link, and track.
