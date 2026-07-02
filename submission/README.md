# StudyOps Capstone Submission Pack

This folder contains materials for the Kaggle AI Agents Intensive Vibe Coding
Capstone Project submission.

Files:

- `kaggle-writeup-draft.md`: draft Kaggle writeup under the 2,500-word limit.
- `video-script.md`: 5-minute demo video script.
- `demo-checklist.md`: recording checklist and demo path.
- `architecture-for-writeup.md`: Mermaid architecture diagram and notes.

The codebase evidence lives in:

- `app/agents/studyops_agents.py`
- `app/workflows/studyops_workflow.py`
- `app/mcp_server.py`
- `frontend/`
- `tests/eval/`

Current public demo links:

- GitHub: https://github.com/dennispang626/studyops-agent
- Frontend: https://studyops-agent.vercel.app

Recommended recording setup:

- Run the public Vercel UI.
- Start the local backend bridge with `scripts/start-local-backend.ps1`.
- In Setup, save `http://127.0.0.1:8000` as the API base URL and click `Test API`.
- Use the local bridge to demonstrate Obsidian note writing, RAG retrieval, and
  SQLite learner memory without exposing private keys or local files.
