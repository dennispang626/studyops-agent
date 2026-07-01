# Phase 9 - GitHub and Vercel Handoff

Phase 9 turned the deployment package into an operator-ready portfolio handoff.
After approval, the public GitHub repository and Vercel production frontend were
created.

## What Was Added

- `GITHUB_VERCEL_HANDOFF.md` with the publish, Vercel, and backend access plan.
- `scripts/preflight.ps1` for repeatable local verification.
- `scripts/release-command-plan.ps1` to print the GitHub and Vercel command
  sequence without running it.
- Phase 9 contract tests.
- Phase output summary in `outputs/`.
- Public GitHub repository.
- Production Vercel frontend.

## Published Links

- GitHub: https://github.com/dennispang626/studyops-agent
- Frontend demo: https://studyops-agent.vercel.app
- Vercel project: https://vercel.com/dennis-heku/studyops-agent

## Recommended Update Flow

1. Run `.\scripts\preflight.ps1`.
2. Commit the UI or agent change.
3. Push to GitHub.
4. Deploy the frontend to Vercel production.
5. Keep backend deployment gated until Google Cloud access and CORS settings are
   ready.

## Access Still Needed

- Optional Google Cloud project and model credentials for backend deployment.

## Deployment Decision

Frontend:

- Ready for Vercel as a static app.

Backend:

- Keep local or deploy to Cloud Run later.
- Do not expose learner memory or API keys in public artifacts.

## Portfolio Outcome

The project now has a clean handoff story:

- code quality checks,
- public demo path,
- source-control publishing path,
- deployment guardrails,
- no-secret checklist,
- capstone link checklist.
