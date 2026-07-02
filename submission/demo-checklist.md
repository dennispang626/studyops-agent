# Demo Checklist

## Before Recording

- Start the local backend bridge:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\start-local-backend.ps1
```

- Open https://studyops-agent.vercel.app.
- Refresh the page.
- Click `Reset` to clear old browser-local memory.
- Confirm the selected certification is `AWS Certified AI Practitioner`.
- On Setup, set API base URL to `http://127.0.0.1:8000`, click `Save API`,
  then click `Test API`.
- Keep the browser zoom around 90-100% so the page fits comfortably.

## Demo Path

1. Agents page
   - Show workflow trace.
   - Mention the six specialist agents.
   - Click `Run workflow`.

2. Setup page
   - Show provider and certification selector.
   - Show learner goal and hours per week.
   - Show backend status as online.
   - Classify an official AWS source.
   - Upload or paste a small trusted note/source if available.
   - Mention unsafe sources are blocked.

3. Study page
   - Click through the domain list.
   - Show active study guidance and checklist.
   - Search notebook context with `responsible AI fairness transparency`.
   - Show cleaned retrieved context, citations, relevance score, and study
     bullets from the backend RAG endpoint.

4. Practice page
   - Answer at least two questions.
   - Intentionally answer one incorrectly.
   - Submit answers.
   - Show per-option feedback.
   - Show weak topics, retry queue, attempts, and confidence score.

5. Export
   - Click `Export` to show evidence can be saved as JSON.

## What to Say

- The project is an MVP, not a guaranteed-pass tool.
- Practice questions are generated exam-style questions, not official questions.
- The safety layer blocks exam dumps and leaked content.
- The study loop is source -> OKF-style Obsidian notes -> Chroma-compatible
  retrieval -> practice -> SQLite memory -> retry.

## Common Demo Risks

- If old local memory appears, click `Reset`.
- If the quiz still looks old, hard-refresh the page.
- If backend status is offline, restart `scripts\start-local-backend.ps1` and
  click `Test API` again.
- If browser file access blocks automation, use the Setup text/source route.
