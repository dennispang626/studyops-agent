"""StudyOps tool functions shared by ADK and the MCP server."""

from __future__ import annotations

from typing import Any

from app.config import ensure_storage_dirs
from app.ingestion.pipeline import ingest_source_url, ingest_study_file
from app.ingestion.source_fetcher import fetch_and_clean_url
from app.knowledge.certifications import (
    CERTIFICATION_CATALOG,
    get_certification_item,
)
from app.rag.index import StudyOpsRagIndex
from app.security.source_trust import classify_source, redact_sensitive_text
from app.storage.obsidian_vault import ObsidianVault
from app.storage.sqlite_store import SQLiteStudyStore
from app.workflows.studyops_workflow import (
    create_study_plan as build_study_plan,
    generate_practice_quiz as build_practice_quiz,
    run_studyops_workflow,
    seed_certification_source_map,
    submit_practice_answers as score_practice_answers,
)


def get_certification_catalog() -> dict[str, Any]:
    """Return supported certifications and official seed sources."""

    return CERTIFICATION_CATALOG


def search_certification_sources(certification: str, query: str = "") -> list[dict[str, Any]]:
    """Return curated official source candidates for the MVP certifications.

    Live search API integration arrives in Phase 4. This curated fallback keeps
    the local demo deterministic and avoids sending users to exam-dump sites.
    """

    item = get_certification_item(certification)
    if item is None:
        return []

    store = SQLiteStudyStore()
    sources = []
    for url in item["official_sources"]:
        trust = classify_source(url=url, title=item["name"], snippet=query)
        store.record_source(
            certification=item["exam_code"],
            url=url,
            title=item["name"],
            trust_level=trust.trust_level,
        )
        sources.append(
            {
                "certification": item["name"],
                "exam_code": item["exam_code"],
                "url": url,
                "trust": trust.to_dict(),
            }
        )
    return sources


def classify_certification_source(
    url: str, title: str = "", snippet: str = ""
) -> dict[str, Any]:
    """Classify a source before it can enter the StudyOps knowledge base."""

    result = classify_source(url=url, title=title, snippet=snippet)
    SQLiteStudyStore().record_source(
        certification="unknown",
        url=url,
        title=title or url,
        trust_level=result.trust_level,
    )
    return result.to_dict()


def fetch_and_clean_source(url: str, title: str = "", snippet: str = "") -> dict[str, Any]:
    """Fetch and clean a trusted source without writing it to the vault."""

    fetched = fetch_and_clean_url(url=url, title=title, snippet=snippet)
    return fetched.to_dict()


def ingest_certification_source(
    certification: str,
    url: str,
    title: str = "",
    domain: str = "",
) -> dict[str, Any]:
    """Fetch a web source, write an Obsidian note, and rebuild the RAG index."""

    ensure_storage_dirs()
    return ingest_source_url(
        certification=certification,
        url=url,
        title=title,
        domain=domain,
    )


def ingest_uploaded_file(
    certification: str,
    file_path: str,
    title: str = "",
    domain: str = "",
) -> dict[str, Any]:
    """Load a local uploaded file, write a note, and rebuild the RAG index."""

    ensure_storage_dirs()
    return ingest_study_file(
        certification=certification,
        file_path=file_path,
        title=title,
        domain=domain,
    )


def rebuild_chroma_index(certification: str = "") -> dict[str, Any]:
    """Rebuild the Chroma-compatible RAG index from Obsidian notes."""

    ensure_storage_dirs()
    return StudyOpsRagIndex().rebuild_from_vault(certification or None)


def generate_rag_context(
    query: str,
    certification: str = "",
    top_k: int = 5,
) -> dict[str, Any]:
    """Retrieve grounded context snippets with citations."""

    ensure_storage_dirs()
    matches = StudyOpsRagIndex().query(
        query=query,
        certification=certification or None,
        top_k=top_k,
    )
    return {
        "query": query,
        "certification": certification,
        "matches": matches,
        "citations": [match["citation"] for match in matches],
    }


def seed_studyops_source_map(certification: str) -> dict[str, Any]:
    """Seed an Obsidian source-map note for a supported certification."""

    ensure_storage_dirs()
    return seed_certification_source_map(certification)


def create_study_plan(
    certification: str,
    learner_goal: str = "",
    hours_per_week: int = 5,
) -> dict[str, Any]:
    """Create a blueprint-driven study plan for a learner."""

    ensure_storage_dirs()
    return build_study_plan(
        certification=certification,
        learner_goal=learner_goal,
        hours_per_week=hours_per_week,
    )


def generate_practice_quiz(
    certification: str,
    query: str = "",
    question_count: int = 5,
) -> dict[str, Any]:
    """Generate safe exam-style practice questions from local RAG context."""

    ensure_storage_dirs()
    return build_practice_quiz(
        certification=certification,
        query=query,
        question_count=question_count,
    )


def submit_practice_answers(
    learner_id: str,
    certification: str,
    submitted_answers: list[dict[str, Any]],
) -> dict[str, Any]:
    """Score practice answers and update learner memory."""

    ensure_storage_dirs()
    return score_practice_answers(
        learner_id=learner_id,
        certification=certification,
        submitted_answers=submitted_answers,
    )


def run_studyops_workflow_tool(
    learner_id: str,
    certification: str,
    learner_goal: str = "",
    hours_per_week: int = 5,
    question_count: int = 5,
) -> dict[str, Any]:
    """Run the focused source-to-quiz StudyOps workflow for the capstone demo."""

    ensure_storage_dirs()
    return run_studyops_workflow(
        learner_id=learner_id,
        certification=certification,
        learner_goal=learner_goal,
        hours_per_week=hours_per_week,
        question_count=question_count,
    )


def write_obsidian_note(
    certification: str,
    title: str,
    body: str,
    source_url: str = "",
    domain: str = "",
) -> dict[str, Any]:
    """Write a redacted Markdown note into the Obsidian vault."""

    ensure_storage_dirs()
    note = ObsidianVault().write_note(
        certification=certification,
        title=title,
        body=redact_sensitive_text(body),
        source_url=source_url or None,
        metadata={"domain": domain},
    )
    return note.to_dict()


def list_obsidian_notes(certification: str = "") -> list[dict[str, str]]:
    """List notes from the Obsidian vault."""

    ensure_storage_dirs()
    return ObsidianVault().list_notes(certification or None)


def search_obsidian_notes(query: str, certification: str = "") -> list[dict[str, str]]:
    """Keyword-search Obsidian notes before semantic RAG arrives in Phase 4."""

    ensure_storage_dirs()
    return ObsidianVault().search_notes(query=query, certification=certification or None)


def record_practice_attempt(
    learner_id: str,
    certification: str,
    score: float,
    answers: list[dict[str, Any]],
) -> dict[str, Any]:
    """Record quiz answers, weak topics, and retry items in SQLite."""

    ensure_storage_dirs()
    attempt = SQLiteStudyStore().record_quiz_attempt(
        learner_id=learner_id,
        certification=certification,
        score=score,
        answers=answers,
    )
    return attempt.to_dict()


def get_learning_memory(learner_id: str, certification: str) -> dict[str, Any]:
    """Return learner progress, weak topics, and retry queue."""

    ensure_storage_dirs()
    return SQLiteStudyStore().get_progress_summary(
        learner_id=learner_id,
        certification=certification,
    )


def get_retry_queue(learner_id: str, certification: str = "") -> list[dict[str, Any]]:
    """Return pending retry items for a learner."""

    ensure_storage_dirs()
    return SQLiteStudyStore().get_retry_queue(
        learner_id=learner_id,
        certification=certification or None,
    )
