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
import os
import logging
from typing import Any

from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from pydantic import BaseModel, Field

from app.app_utils.telemetry import setup_telemetry
from app.app_utils.typing import Feedback
from app.workflows.studyops_workflow import (
    create_study_plan,
    generate_practice_quiz,
    run_studyops_workflow,
    submit_practice_answers,
)

setup_telemetry()
logger = logging.getLogger(__name__)
allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None

artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=True,
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


class StudyOpsSubmitRequest(BaseModel):
    """Request body for practice answer scoring."""

    learner_id: str = Field(default="demo-learner")
    certification: str = Field(default="AIF-C01")
    submitted_answers: list[dict[str, Any]] = Field(default_factory=list)


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
