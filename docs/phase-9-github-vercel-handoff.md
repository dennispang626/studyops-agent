# Phase 9 - GitHub and Vercel Handoff

Phase 9 turns the deployment package into an operator-ready portfolio handoff.
No external credentials were used and no live deployment was performed.

## What Was Added

- `GITHUB_VERCEL_HANDOFF.md` with the publish, Vercel, and backend access plan.
- `scripts/preflight.ps1` for repeatable local verification.
- `scripts/release-command-plan.ps1` to print the GitHub and Vercel command
  sequence without running it.
- Phase 9 contract tests.
- Phase output summary in `outputs/`.

## Recommended Publish Flow

1. Run `.\scripts\preflight.ps1`.
2. Initialize Git locally.
3. Commit the MVP package.
4. Authenticate with GitHub CLI.
5. Create and push the repo with `gh repo create`.
6. Import the repo into Vercel with `frontend/` as the project root.
7. Keep backend deployment gated until Google Cloud access and CORS settings are
   ready.

## Access Still Needed

- GitHub account or organization access.
- Vercel account or team access.
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

