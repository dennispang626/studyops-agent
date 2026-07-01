# Architecture for Writeup

```mermaid
flowchart TD
    U["Learner"] --> UI["Vercel-ready StudyOps UI"]
    UI --> API["FastAPI StudyOps routes"]
    API --> ROOT["ADK Root Agent: StudyOps Orchestrator"]

    ROOT --> SC["Source Curator Agent"]
    ROOT --> TF["Trust and Noise Filter Agent"]
    ROOT --> KA["Knowledge Architect Agent"]
    ROOT --> SP["Study Planner Agent"]
    ROOT --> PC["Practice Coach Agent"]
    ROOT --> ER["Examiner and Remediation Agent"]

    SC --> SOURCES["Official AWS sources and user uploads"]
    TF --> SAFE["Source trust, exam-dump blocking, prompt-injection checks"]
    KA --> OBS["Obsidian Markdown vault"]
    OBS --> RAG["Chroma-compatible RAG index"]
    SP --> PLAN["Domain study plan"]
    PC --> QUIZ["Generated exam-style practice questions"]
    ER --> MEM["SQLite attempts, weak topics, retry queue"]

    RAG --> PC
    MEM --> SP
    MEM --> ER
```

## Key Data Stores

- Obsidian vault: human-readable Markdown knowledge base.
- Chroma-compatible index: retrieval over notes, with JSON fallback for local demos.
- SQLite: learner attempts, weak topics, confidence signal, and retry queue.

## Safety Boundary

All web and uploaded content is treated as untrusted. The trust layer blocks
exam-dump language, flags prompt-injection phrases, and redacts obvious secrets
or PII before storage.

