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

    SC --> SOURCES["Raw URLs, PDFs, and learner uploads"]
    SOURCES --> EXTRACT["Extracted source text"]
    EXTRACT --> TF
    TF --> SAFE["Source trust, exam-dump blocking, prompt-injection checks"]
    SAFE --> KA
    KA --> OBS["OKF-style Obsidian Markdown wiki"]
    OBS --> RAG["Chroma-compatible vector index"]
    RAG --> RET["Cited RAG retrieval"]
    SP --> PLAN["Domain study plan"]
    PC --> QUIZ["Generated exam-style practice questions"]
    ER --> MEM["SQLite attempts, weak topics, retry queue"]

    RET --> PC
    RET --> SP
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
