# StudyOps GitHub and Vercel Handoff

Phase 9 prepares StudyOps Agent for portfolio publishing. It does not push,
deploy, or use private credentials.

## Current State

- The local `studyops-agent/` folder is deployment-ready but is not yet a Git
  repository.
- The frontend can be deployed as a static Vercel project from `frontend/`.
- The backend is packaged for a later Cloud Run deployment.
- No GitHub, Vercel, or Google Cloud credentials have been used in this phase.

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

Use a private repo while iterating if you are still polishing the capstone. Use a
public repo before Kaggle submission if you want judges to access the code
directly.

```powershell
git init
git branch -M main
git add .
git commit -m "Initial StudyOps Agent capstone MVP"
gh auth login
gh repo create studyops-agent --public --source . --remote origin --push
```

If you prefer private first:

```powershell
gh repo create studyops-agent --private --source . --remote origin --push
```

Before making the repo public, re-check:

- `.env` is not committed.
- `data/sqlite/studyops.db` is not committed.
- generated Chroma index files are not committed.
- generated Obsidian vault notes are not committed unless intentionally curated.
- no API keys, passwords, private files, or real exam dump content are present.

## Vercel Frontend Plan

Create a Vercel project from the GitHub repo with these settings:

```text
Root directory: frontend
Framework preset: Other
Build command: none
Output directory: .
```

The frontend works without a backend in browser-local demo mode.

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

