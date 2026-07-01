# StudyOps Deployment Guide

StudyOps Agent is packaged as a split frontend/backend project:

- `frontend/`: static Vercel-ready web UI.
- `app/`: Python FastAPI + ADK backend.
- `submission/`: Kaggle writeup and demo materials.

Phase 8 prepares deployment packaging only. Do not deploy production services
until tests pass and the deployment target is explicitly approved.

## Published Frontend

- GitHub repository: https://github.com/dennispang626/studyops-agent
- Production frontend: https://studyops-agent.vercel.app
- Vercel project: https://vercel.com/dennis-heku/studyops-agent

The backend has not been deployed. The production frontend currently runs in
browser-local demo mode.

## 1. GitHub Packaging

Recommended repository root: `studyops-agent/`.

Before pushing:

```powershell
python -m unittest discover -s tests\unit
node --check frontend\app.js
```

Files already prepared:

- `.gitignore`
- `.env.example`
- `.github/workflows/ci.yml`
- `DEPLOYMENT.md`
- `frontend/package.json`
- `frontend/vercel.json`

Do not commit:

- `.env`
- API keys
- `data/sqlite/studyops.db`
- `data/chroma/*`
- local Obsidian generated folders under `data/obsidian_vault/*/`
- eval artifacts under `artifacts/`

## 2. Vercel Frontend

Deploy the `frontend/` directory as a static Vercel project.

Recommended Vercel settings:

- Framework preset: Other
- Root directory: `frontend`
- Build command: none
- Output directory: `.`

The frontend works in browser-local demo mode without backend access.

When a public backend exists, configure:

```text
STUDYOPS_API_BASE_URL=https://your-backend.example.com
```

If using the static version without build-time environment injection, open the
browser console and set:

```js
localStorage.setItem("studyops_api_base", "https://your-backend.example.com")
```

Then refresh the page.

## 3. Backend Options

The scaffold manifest currently has:

```text
deployment_target: none
session_type: in_memory
```

Recommended next backend target for this MVP: Cloud Run.

Why Cloud Run:

- Works well with FastAPI.
- Supports custom containers.
- Easier to connect from Vercel.
- Can later add Pub/Sub or scheduled workflows if StudyOps becomes ambient.

Agent Runtime is also possible later if the project moves toward managed agent
hosting and Gemini Enterprise registration.

## 4. Backend Local Run

After installing dependencies:

```powershell
uv sync
uv run uvicorn app.fast_api_app:app --host 0.0.0.0 --port 8080
```

Useful endpoints:

- `POST /api/studyops/workflow`
- `POST /api/studyops/study-plan`
- `POST /api/studyops/practice-quiz`
- `POST /api/studyops/practice-submit`

## 5. Backend Container

The Dockerfile builds the Python backend from `pyproject.toml` with
`uv sync --no-dev`. Add and commit a `uv.lock` later if you want fully frozen
container dependency resolution.

Example:

```bash
docker build -t studyops-agent-backend .
docker run -p 8080:8080 --env-file .env studyops-agent-backend
```

## 6. Required Environment Variables

Local storage:

```text
STUDYOPS_OBSIDIAN_VAULT=data/obsidian_vault
STUDYOPS_CHROMA_DIR=data/chroma
STUDYOPS_SQLITE_PATH=data/sqlite/studyops.db
```

Model calls:

```text
GOOGLE_API_KEY=...
```

or Vertex AI:

```text
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=...
GOOGLE_CLOUD_LOCATION=global
```

CORS for deployed frontend:

```text
ALLOW_ORIGINS=https://your-studyops-demo.vercel.app
```

## 7. Eval Before Deployment

Run deterministic checks:

```powershell
python -m unittest discover -s tests\unit
node --check frontend\app.js
```

After full ADK dependencies and model credentials are available:

```bash
agents-cli eval generate
agents-cli eval grade
```

Do not claim production quality until eval results are reviewed.

## 8. Release Checklist

- Tests pass.
- Frontend opens locally.
- Demo flow works: Agents -> Setup -> Study -> Practice.
- No secrets are committed.
- Kaggle writeup and video script are current.
- Vercel frontend URL is public.
- Backend URL is public only if login-free access is intended.
- Generated questions are clearly labeled as exam-style practice, not official questions.
