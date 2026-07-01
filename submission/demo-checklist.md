# Demo Checklist

## Before Recording

- Open `frontend/index.html`.
- Refresh the page.
- Click `Reset` to clear old browser-local memory.
- Confirm the selected certification is `AWS Certified AI Practitioner`.
- Keep the browser zoom around 90-100% so the page fits comfortably.

## Demo Path

1. Agents page
   - Show workflow trace.
   - Mention the six specialist agents.
   - Click `Run workflow`.

2. Setup page
   - Show provider and certification selector.
   - Show learner goal and hours per week.
   - Classify an official AWS source.
   - Mention unsafe sources are blocked.

3. Study page
   - Click through the domain list.
   - Show active study guidance and checklist.
   - Search notebook context with `responsible AI`.
   - Show retrieved context and citations.

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
- The study loop is source -> notes -> RAG -> practice -> memory -> retry.

## Common Demo Risks

- If old local memory appears, click `Reset`.
- If the quiz still looks old, hard-refresh the page.
- If browser file access blocks automation, open the file manually.

