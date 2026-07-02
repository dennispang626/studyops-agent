# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, UploadFile
from google.adk.cli.fast_api import get_fast_api_app
from pydantic import BaseModel, Field

from app.app_utils.telemetry import setup_telemetry
from app.app_utils.typing import Feedback
from app.config import ensure_storage_dirs
from app.ingestion.pipeline import ingest_source_url, ingest_study_file
from app.rag.index import StudyOpsRagIndex
from app.storage.sqlite_store import SQLiteStudyStore
from app.workflows.studyops_workflow import (
    create_study_plan,
    generate_practice_quiz,
    run_studyops_workflow,
    submit_practice_answers,
)

setup_telemetry()
logger = logging.getLogger(__name__)
DEFAULT_ALLOW_ORIGINS = [
    "https://studyops-agent.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "null",
]


def parse_allow_origins() -> list[str]:
    """Return explicit frontend origins allowed to call the local API bridge."""

    raw_origins = os.getenv("ALLOW_ORIGINS", "")
    if raw_origins.strip():
        return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return DEFAULT_ALLOW_ORIGINS


allow_origins = parse_allow_origins()

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None

artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None
otel_to_cloud = os.getenv("STUDYOPS_OTEL_TO_CLOUD", "false").lower() in {
    "1",
    "true",
    "yes",
}

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=otel_to_cloud,
)
app.title = "studyops-agent"
app.description = "API for interacting with the Agent studyops-agent"


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    logger.info("feedback=%s", feedback.model_dump())
    return {"status": "success"}


class StudyOpsWorkflowRequest(BaseModel):
    """Request body for the web UI workflow endpoint."""

    learner_id: str = Field(default="demo-learner")
    certification: str = Field(default="AIF-C01")
    learner_goal: str = Field(default="")
    uploaded_file_paths: list[str] = Field(default_factory=list)
    hours_per_week: int = Field(default=5, ge=1, le=40)
    question_count: int = Field(default=5, ge=1, le=10)


class StudyOpsPlanRequest(BaseModel):
    """Request body for study plan previews."""

    certification: str = Field(default="AIF-C01")
    learner_goal: str = Field(default="")
    hours_per_week: int = Field(default=5, ge=1, le=40)


class StudyOpsQuizRequest(BaseModel):
    """Request body for practice quiz generation."""

    certification: str = Field(default="AIF-C01")
    query: str = Field(default="")
    question_count: int = Field(default=5, ge=1, le=10)


class StudyOpsRagContextRequest(BaseModel):
    """Request body for retrieving cited RAG context."""

    certification: str = Field(default="AIF-C01")
    query: str = Field(default="")
    top_k: int = Field(default=5, ge=1, le=10)


class StudyOpsIngestUrlRequest(BaseModel):
    """Request body for URL ingestion into the OKF-style wiki."""

    certification: str = Field(default="AIF-C01")
    url: str = Field()
    title: str = Field(default="")
    domain: str = Field(default="")


class StudyOpsSubmitRequest(BaseModel):
    """Request body for practice answer scoring."""

    learner_id: str = Field(default="demo-learner")
    certification: str = Field(default="AIF-C01")
    submitted_answers: list[dict[str, Any]] = Field(default_factory=list)


@app.get("/api/studyops/health")
def studyops_health_endpoint() -> dict[str, Any]:
    """Return local bridge readiness without exposing secret values."""

    paths = ensure_storage_dirs()
    SQLiteStudyStore()
    rag_index = StudyOpsRagIndex()
    markdown_notes = [
        path
        for path in paths.obsidian_vault.rglob("*.md")
        if path.name.lower() != "readme.md"
    ]
    source_notes = list((paths.obsidian_vault / "sources").glob("*.md"))
    certificates_dir = paths.obsidian_vault / "certificates"
    certificates = (
        [path.name for path in certificates_dir.iterdir() if path.is_dir()]
        if certificates_dir.exists()
        else []
    )

    return {
        "status": "ok",
        "service": "studyops-local-bridge",
        "gemini_api_key_configured": bool(os.getenv("GOOGLE_API_KEY")),
        "storage": {
            "obsidian_vault_ready": paths.obsidian_vault.exists(),
            "vault_notes": len(markdown_notes),
            "source_notes": len(source_notes),
            "certificates": sorted(certificates),
            "rag_index_ready": rag_index.fallback_path.exists(),
            "rag_index_backend": "json-fallback"
            if rag_index.fallback_path.exists()
            else "pending",
            "sqlite_ready": paths.sqlite_path.exists(),
        },
        "routes": [
            "/api/studyops/workflow",
            "/api/studyops/rag-context",
            "/api/studyops/ingest-url",
            "/api/studyops/ingest-file",
            "/api/studyops/practice-submit",
        ],
    }


@app.post("/api/studyops/workflow")
def run_studyops_workflow_endpoint(request: StudyOpsWorkflowRequest) -> dict[str, Any]:
    """Run the deterministic StudyOps workflow for the frontend."""

    return run_studyops_workflow(
        learner_id=request.learner_id,
        certification=request.certification,
        learner_goal=request.learner_goal,
        uploaded_file_paths=request.uploaded_file_paths,
        hours_per_week=request.hours_per_week,
        question_count=request.question_count,
    )


@app.post("/api/studyops/study-plan")
def create_study_plan_endpoint(request: StudyOpsPlanRequest) -> dict[str, Any]:
    """Create a blueprint-driven study plan for the frontend."""

    return create_study_plan(
        certification=request.certification,
        learner_goal=request.learner_goal,
        hours_per_week=request.hours_per_week,
    )


@app.post("/api/studyops/practice-quiz")
def generate_practice_quiz_endpoint(request: StudyOpsQuizRequest) -> dict[str, Any]:
    """Generate safe exam-style practice questions for the frontend."""

    return generate_practice_quiz(
        certification=request.certification,
        query=request.query,
        question_count=request.question_count,
    )


@app.post("/api/studyops/rag-context")
def retrieve_rag_context_endpoint(request: StudyOpsRagContextRequest) -> dict[str, Any]:
    """Retrieve cited context from the local Obsidian/RAG index."""

    ensure_storage_dirs()
    query = request.query.strip()
    matches = StudyOpsRagIndex().query(
        query=query,
        certification=request.certification,
        top_k=request.top_k,
    )
    safe_matches = []
    for match in matches:
        metadata = match.get("metadata", {}) if isinstance(match, dict) else {}
        safe_metadata = {
            "path": metadata.get("path", ""),
            "title": metadata.get("title", ""),
            "certification": metadata.get("certification", ""),
            "type": metadata.get("type", ""),
            "tags": metadata.get("tags", ""),
            "review_status": metadata.get("review_status", ""),
        }
        safe_matches.append(
            {
                "text": match.get("text", ""),
                "metadata": safe_metadata,
                "score": match.get("score", 0),
                "citation": match.get("citation", "") or safe_metadata["path"],
                "backend": match.get("backend", "unknown"),
            }
        )

    return {
        "query": query,
        "certification": request.certification,
        "top_k": request.top_k,
        "matches": safe_matches,
        "citations": [match["citation"] for match in safe_matches],
        "retrieval_backend": safe_matches[0]["backend"] if safe_matches else "none",
    }


@app.post("/api/studyops/ingest-url")
def ingest_source_url_endpoint(request: StudyOpsIngestUrlRequest) -> dict[str, Any]:
    """Ingest a trusted URL into Obsidian Markdown and the RAG index."""

    return ingest_source_url(
        certification=request.certification,
        url=request.url,
        title=request.title,
        domain=request.domain,
    )


@app.post("/api/studyops/ingest-file")
async def ingest_file_endpoint(
    file: UploadFile = File(...),
    certification: str = Form(default="AIF-C01"),
    title: str = Form(default=""),
    domain: str = Form(default=""),
) -> dict[str, Any]:
    """Ingest an uploaded file into Obsidian Markdown and the RAG index."""

    suffix = Path(file.filename or "upload.txt").suffix or ".txt"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as handle:
        temp_path = Path(handle.name)
        handle.write(await file.read())

    try:
        return ingest_study_file(
            certification=certification,
            file_path=str(temp_path),
            title=title or Path(file.filename or "Uploaded study file").stem,
            domain=domain,
        )
    finally:
        temp_path.unlink(missing_ok=True)


@app.post("/api/studyops/practice-submit")
def submit_practice_answers_endpoint(request: StudyOpsSubmitRequest) -> dict[str, Any]:
    """Score practice answers and update learner memory."""

    return submit_practice_answers(
        learner_id=request.learner_id,
        certification=request.certification,
        submitted_answers=request.submitted_answers,
    )


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
