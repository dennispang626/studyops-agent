"""Ingestion pipeline from source/file text to Obsidian notes and RAG index."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from app.ingestion.file_loader import load_study_file
from app.ingestion.source_fetcher import FetchedSource, fetch_and_clean_url
from app.knowledge.certifications import get_exam_code
from app.rag.index import StudyOpsRagIndex
from app.storage.obsidian_vault import ObsidianVault, slugify


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+-]{2,}")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
STOP_WORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "aws",
    "can",
    "for",
    "from",
    "has",
    "have",
    "into",
    "its",
    "may",
    "not",
    "that",
    "the",
    "this",
    "with",
    "you",
    "your",
}


def _top_terms(text: str, limit: int = 12) -> list[str]:
    tokens = [
        token.lower()
        for token in TOKEN_RE.findall(text)
        if token.lower() not in STOP_WORDS
    ]
    return [token for token, _ in Counter(tokens).most_common(limit)]


def _summary_bullets(text: str, limit: int = 6) -> list[str]:
    sentences = [sentence.strip() for sentence in SENTENCE_RE.split(text) if sentence.strip()]
    bullets = []
    for sentence in sentences:
        if 50 <= len(sentence) <= 280:
            bullets.append(sentence)
        if len(bullets) >= limit:
            break
    if bullets:
        return bullets
    return [text[:280].strip()] if text.strip() else []


def build_study_note_body(
    certification: str,
    title: str,
    text: str,
    source_url: str = "",
    trust_level: str = "uploaded",
) -> str:
    """Create deterministic, reviewable study-note Markdown from source text."""

    terms = _top_terms(text)
    bullets = _summary_bullets(text)
    term_lines = "\n".join(f"- {term}" for term in terms) or "- No key terms found."
    concept_lines = (
        "\n".join(f"- [[../concepts/{slugify(term)}|{term}]]" for term in terms[:6])
        or "- No concept links generated."
    )
    bullet_lines = "\n".join(f"- {bullet}" for bullet in bullets) or "- No summary generated."

    citation = source_url or "User uploaded file"
    return (
        f"## Source\n\n"
        f"- Certification: {certification}\n"
        f"- Trust level: {trust_level}\n"
        f"- Citation: {citation}\n\n"
        f"## Study Summary\n\n{bullet_lines}\n\n"
        f"## Concept Links\n\n{concept_lines}\n\n"
        f"## Key Terms\n\n{term_lines}\n\n"
        f"## Source Extract\n\n{text[:5000].strip()}\n"
    )


def ingest_fetched_source(
    certification: str,
    fetched: FetchedSource,
    domain: str = "",
) -> dict[str, Any]:
    """Write a fetched source into Obsidian and rebuild the local RAG index."""

    exam_code = get_exam_code(certification)
    vault = ObsidianVault()
    vault.ensure_okf_structure(exam_code)
    body = build_study_note_body(
        certification=exam_code,
        title=fetched.title,
        text=fetched.text,
        source_url=fetched.url,
        trust_level=fetched.trust.trust_level,
    )
    note = vault.write_source_note(
        certification=exam_code,
        title=fetched.title,
        body=body,
        source_url=fetched.url,
        domain=domain,
        trust_level=fetched.trust.trust_level,
        source_kind="web_source",
        metadata={
            "prompt_injection_detected": str(fetched.prompt_injection_detected),
            "fetched_at": fetched.fetched_at,
        },
    )
    index_result = StudyOpsRagIndex().rebuild_from_vault(certification=exam_code)
    return {"note": note.to_dict(), "index": index_result}


def ingest_source_url(
    certification: str,
    url: str,
    title: str = "",
    domain: str = "",
) -> dict[str, Any]:
    """Fetch, clean, write, and index one web source."""

    fetched = fetch_and_clean_url(url=url, title=title)
    return ingest_fetched_source(certification=certification, fetched=fetched, domain=domain)


def ingest_study_file(
    certification: str,
    file_path: str,
    title: str = "",
    domain: str = "",
) -> dict[str, Any]:
    """Load a local file, write it to Obsidian, and rebuild the RAG index."""

    exam_code = get_exam_code(certification)
    vault = ObsidianVault()
    vault.ensure_okf_structure(exam_code)
    loaded = load_study_file(file_path=file_path, title=title)
    body = build_study_note_body(
        certification=exam_code,
        title=loaded.title,
        text=loaded.text,
        trust_level="user_uploaded",
    )
    note = vault.write_source_note(
        certification=exam_code,
        title=loaded.title,
        body=body,
        source_url=loaded.path,
        domain=domain,
        trust_level="user_uploaded",
        source_kind="uploaded_source",
        metadata={"loaded_at": loaded.loaded_at},
    )
    index_result = StudyOpsRagIndex().rebuild_from_vault(certification=exam_code)
    return {"note": note.to_dict(), "index": index_result}
