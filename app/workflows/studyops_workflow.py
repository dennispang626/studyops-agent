"""Deterministic StudyOps workflow used by ADK tools and demos.

The LLM-facing agents can decide when to call these functions, but the core
study loop is deterministic so the capstone demo and tests are reproducible.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.config import ensure_storage_dirs
from app.ingestion.pipeline import ingest_study_file
from app.knowledge.certifications import (
    get_blueprint,
    get_certification_item,
    get_exam_code,
)
from app.rag.index import StudyOpsRagIndex
from app.security.source_trust import classify_source, redact_sensitive_text
from app.storage.obsidian_vault import ObsidianVault
from app.storage.sqlite_store import SQLiteStudyStore


PRACTICE_DISCLAIMER = "Generated exam-style practice, not official questions."

QUESTION_BANK: dict[str, list[dict[str, Any]]] = {
    "AIF-C01": [
        {
            "topic": "Fundamentals of AI and ML",
            "difficulty": "Foundation",
            "stem": (
                "A support team has thousands of labeled historical tickets and "
                "wants to route new tickets to the correct queue automatically. "
                "Which machine learning approach best fits this use case?"
            ),
            "options": {
                "A": "Supervised learning",
                "B": "Unsupervised clustering without labels",
                "C": "Manual rule writing for every possible ticket",
                "D": "Reinforcement learning with a reward signal",
            },
            "correct": "A",
            "option_explanations": {
                "A": "The historical tickets include labels, so the model can learn from known outcomes.",
                "B": "Clustering can discover groups, but it does not directly learn from existing queue labels.",
                "C": "Manual rules are brittle and do not use the labeled training data effectively.",
                "D": "Reinforcement learning is for sequential decisions with rewards, not basic labeled classification.",
            },
        },
        {
            "topic": "Fundamentals of generative AI",
            "difficulty": "Foundation",
            "stem": (
                "A marketing team wants to draft product descriptions from short "
                "prompts without training its own model. Which AWS service is the "
                "most appropriate starting point?"
            ),
            "options": {
                "A": "AWS CloudTrail",
                "B": "Amazon Bedrock",
                "C": "Amazon Route 53",
                "D": "AWS Cost Explorer",
            },
            "correct": "B",
            "option_explanations": {
                "A": "CloudTrail records account activity and API events; it is not used to generate text.",
                "B": "Amazon Bedrock provides access to foundation models for generative AI use cases.",
                "C": "Route 53 is DNS networking infrastructure, not a generative AI service.",
                "D": "Cost Explorer analyzes spend and usage; it does not create generated content.",
            },
        },
        {
            "topic": "Applications of foundation models",
            "difficulty": "Scenario",
            "stem": (
                "A company is building a customer-service assistant that must answer "
                "only from approved product documents. Which design choice best "
                "reduces unsupported answers?"
            ),
            "options": {
                "A": "Increase the response length for every answer",
                "B": "Use retrieval from approved documents and cite the retrieved context",
                "C": "Remove all evaluation checks to make the assistant faster",
                "D": "Let the model answer from general knowledge when documents are missing",
            },
            "correct": "B",
            "option_explanations": {
                "A": "Longer answers can still be unsupported if they are not grounded in approved content.",
                "B": "Retrieval-grounded generation helps constrain answers to approved sources and gives reviewers citations.",
                "C": "Removing evaluations increases quality and safety risk.",
                "D": "General knowledge can conflict with current product documents.",
            },
        },
        {
            "topic": "Guidelines for responsible AI",
            "difficulty": "Scenario",
            "stem": (
                "An HR team wants to use an AI assistant to summarize candidate "
                "feedback. Which practice best supports responsible AI for this workflow?"
            ),
            "options": {
                "A": "Use the assistant output as the final hiring decision",
                "B": "Avoid reviewing the assistant because summaries are always objective",
                "C": "Review outputs for bias, keep humans in the decision loop, and protect sensitive data",
                "D": "Store all candidate data in prompts so the assistant has maximum context",
            },
            "correct": "C",
            "option_explanations": {
                "A": "High-impact decisions need human accountability and should not rely only on generated output.",
                "B": "AI summaries can contain bias or omissions, so review is still necessary.",
                "C": "Bias review, human oversight, and data protection are core responsible AI practices.",
                "D": "Including unnecessary sensitive data increases privacy and security risk.",
            },
        },
        {
            "topic": "Security, compliance, and governance for AI solutions",
            "difficulty": "Scenario",
            "stem": (
                "A team uses a generative AI application on AWS and needs to restrict "
                "who can invoke models. Which control should they configure first?"
            ),
            "options": {
                "A": "Public access to the model endpoint",
                "B": "IAM permissions that follow least privilege",
                "C": "A larger context window",
                "D": "A lower model temperature",
            },
            "correct": "B",
            "option_explanations": {
                "A": "Public access would increase risk and is the opposite of controlled access.",
                "B": "IAM policies are used to control who can perform actions on AWS resources.",
                "C": "Context length affects prompt capacity, not identity-based authorization.",
                "D": "Temperature affects response randomness, not access control.",
            },
        },
    ],
    "CLF-C02": [
        {
            "topic": "Cloud concepts",
            "difficulty": "Foundation",
            "stem": (
                "A startup wants to avoid buying servers before knowing whether its "
                "application will be popular. Which cloud benefit does this best describe?"
            ),
            "options": {
                "A": "Trade fixed expense for variable expense",
                "B": "Manually patch all physical hosts",
                "C": "Commit to maximum capacity up front",
                "D": "Move all responsibility from the customer to AWS",
            },
            "correct": "A",
            "option_explanations": {
                "A": "Cloud pricing lets customers pay for resources as they use them instead of buying data center capacity up front.",
                "B": "Manual physical host management is reduced, but that is not the benefit described here.",
                "C": "The cloud helps avoid over-provisioning capacity in advance.",
                "D": "The shared responsibility model still gives customers responsibilities.",
            },
        },
        {
            "topic": "Security and compliance",
            "difficulty": "Scenario",
            "stem": (
                "Under the AWS shared responsibility model, which task is typically "
                "the customer's responsibility?"
            ),
            "options": {
                "A": "Maintaining AWS global infrastructure",
                "B": "Replacing physical disks in AWS data centers",
                "C": "Managing IAM users and permissions in the AWS account",
                "D": "Securing the physical facilities that host AWS Regions",
            },
            "correct": "C",
            "option_explanations": {
                "A": "AWS is responsible for the security of the cloud, including global infrastructure.",
                "B": "AWS manages physical hardware in its data centers.",
                "C": "Customers manage identities, permissions, and access decisions inside their own accounts.",
                "D": "AWS handles physical security for its facilities.",
            },
        },
        {
            "topic": "Cloud technology and services",
            "difficulty": "Foundation",
            "stem": (
                "A company needs durable object storage for images, documents, and "
                "backups. Which AWS service should it choose?"
            ),
            "options": {
                "A": "Amazon S3",
                "B": "Amazon EC2 Auto Scaling",
                "C": "AWS Lambda",
                "D": "Amazon Route 53",
            },
            "correct": "A",
            "option_explanations": {
                "A": "Amazon S3 is object storage designed for durable storage of files and backups.",
                "B": "EC2 Auto Scaling adjusts compute capacity, not object storage.",
                "C": "Lambda runs code without managing servers; it is not object storage.",
                "D": "Route 53 provides DNS and routing features.",
            },
        },
        {
            "topic": "Cloud technology and services",
            "difficulty": "Scenario",
            "stem": (
                "A developer wants to run code in response to events without managing "
                "servers. Which AWS service is the best fit?"
            ),
            "options": {
                "A": "Amazon VPC",
                "B": "AWS Lambda",
                "C": "AWS Organizations",
                "D": "AWS Artifact",
            },
            "correct": "B",
            "option_explanations": {
                "A": "Amazon VPC provides networking isolation, not serverless event-driven code execution.",
                "B": "AWS Lambda runs code in response to events without requiring server management.",
                "C": "AWS Organizations manages multiple AWS accounts.",
                "D": "AWS Artifact provides compliance reports and agreements.",
            },
        },
        {
            "topic": "Billing, pricing, and support",
            "difficulty": "Foundation",
            "stem": (
                "A finance team wants to estimate monthly AWS costs before launching "
                "a workload. Which tool should it use?"
            ),
            "options": {
                "A": "AWS Pricing Calculator",
                "B": "AWS CloudTrail",
                "C": "Amazon CloudWatch Logs",
                "D": "AWS Identity and Access Management",
            },
            "correct": "A",
            "option_explanations": {
                "A": "AWS Pricing Calculator helps estimate costs before deployment.",
                "B": "CloudTrail records API activity and account events.",
                "C": "CloudWatch Logs stores and analyzes logs, not pre-launch cost estimates.",
                "D": "IAM manages access and permissions.",
            },
        },
    ],
}


@dataclass(frozen=True)
class WorkflowTraceStep:
    """A visible trace step for the capstone demo and writeup."""

    agent: str
    action: str
    output: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-serializable trace step."""

        return asdict(self)


def _bounded_int(value: int, minimum: int, maximum: int) -> int:
    return min(max(int(value), minimum), maximum)


def _official_sources(certification: str) -> list[str]:
    item = get_certification_item(certification)
    if item is None:
        return []
    return [str(url) for url in item.get("official_sources", [])]


def _source_map_body(
    certification: str,
    blueprint: dict[str, Any],
    official_sources: list[str],
) -> str:
    domain_lines = "\n".join(f"- {domain}" for domain in blueprint["domains"])
    source_lines = "\n".join(f"- {url}" for url in official_sources)
    focus_lines = "\n".join(f"- {term}" for term in blueprint["focus_terms"])
    if not source_lines:
        source_lines = "- User-provided sources only until official sources are added."

    return (
        "## Purpose\n\n"
        f"This source map seeds StudyOps for {blueprint['name']} ({certification}). "
        "It keeps the first demo grounded in official certification pages and "
        "high-level exam domains instead of copied exam questions.\n\n"
        "## Safety Rules\n\n"
        "- Do not use leaked, copied, or real exam dump questions.\n"
        "- Treat web content as untrusted data until the trust filter approves it.\n"
        "- Cite sources when creating notes, study plans, and practice feedback.\n\n"
        "## Exam Domains\n\n"
        f"{domain_lines}\n\n"
        "## Retrieval Focus Terms\n\n"
        f"{focus_lines}\n\n"
        "## Official Source Candidates\n\n"
        f"{source_lines}\n"
    )


def seed_certification_source_map(certification: str) -> dict[str, Any]:
    """Create a safe starter source map note and rebuild the RAG index."""

    ensure_storage_dirs()
    exam_code = get_exam_code(certification)
    blueprint = get_blueprint(exam_code)
    sources = _official_sources(certification)
    store = SQLiteStudyStore()
    source_records: list[dict[str, Any]] = []

    for url in sources:
        trust = classify_source(url=url, title=blueprint["name"])
        source_records.append(trust.to_dict())
        store.record_source(
            certification=exam_code,
            url=url,
            title=blueprint["name"],
            trust_level=trust.trust_level,
        )

    note = ObsidianVault().write_note(
        certification=exam_code,
        title=f"{blueprint['name']} Official Source Map",
        body=_source_map_body(exam_code, blueprint, sources),
        source_url=sources[0] if sources else None,
        metadata={"domain": "source_map", "trust_level": "official"},
    )
    index = StudyOpsRagIndex().rebuild_from_vault(certification=exam_code)
    return {
        "certification": exam_code,
        "note": note.to_dict(),
        "index": index,
        "sources": source_records,
    }


def create_study_plan(
    certification: str,
    learner_goal: str = "",
    hours_per_week: int = 5,
) -> dict[str, Any]:
    """Create a structured study plan from the certification blueprint."""

    ensure_storage_dirs()
    exam_code = get_exam_code(certification)
    blueprint = get_blueprint(exam_code)
    weekly_hours = _bounded_int(hours_per_week, 1, 40)
    domains = list(blueprint["domains"])
    domain_hours = max(1, round(weekly_hours / max(len(domains), 1), 1))

    weeks = []
    for index, domain in enumerate(domains, start=1):
        weeks.append(
            {
                "week": index,
                "focus": domain,
                "estimated_hours": domain_hours,
                "tasks": [
                    "Review official-source notes and RAG citations.",
                    "Create concise Obsidian notes with examples and key terms.",
                    "Answer generated exam-style practice questions.",
                    "Retry missed topics until confidence improves.",
                ],
            }
        )

    return {
        "certification": exam_code,
        "certification_name": blueprint["name"],
        "learner_goal": redact_sensitive_text(learner_goal).strip(),
        "hours_per_week": weekly_hours,
        "weekly_plan": weeks,
        "daily_loop": [
            "Curate or upload one trusted source.",
            "Convert useful content into an Obsidian study note.",
            "Retrieve grounded context from the RAG index.",
            "Practice generated exam-style questions.",
            "Record weak topics and retry missed areas.",
        ],
        "success_metrics": [
            "At least one cited note per blueprint domain.",
            "Retry queue shrinks after each practice round.",
            "Weak-topic mastery score trends upward over time.",
        ],
    }


def _question_template(exam_code: str, topic: str, question_index: int) -> dict[str, Any]:
    bank = QUESTION_BANK.get(exam_code, QUESTION_BANK["AIF-C01"])
    for question in bank:
        if question["topic"] == topic:
            return question
    return bank[(question_index - 1) % len(bank)]


def _make_question(
    exam_code: str,
    topic: str,
    question_index: int,
    citation: str,
) -> dict[str, Any]:
    template = _question_template(exam_code, topic, question_index)
    correct_answer = str(template["correct"])
    question_id = f"{exam_code}-PRACTICE-{question_index:03d}"
    return {
        "question_id": question_id,
        "certification": exam_code,
        "topic": template["topic"],
        "difficulty": template["difficulty"],
        "question": template["stem"],
        "options": template["options"],
        "correct_answer": correct_answer,
        "explanation": template["option_explanations"][correct_answer],
        "option_explanations": template["option_explanations"],
        "citation": citation,
    }


def generate_practice_quiz(
    certification: str,
    query: str = "",
    question_count: int = 5,
) -> dict[str, Any]:
    """Generate deterministic, source-grounded practice questions."""

    ensure_storage_dirs()
    exam_code = get_exam_code(certification)
    blueprint = get_blueprint(exam_code)
    if not ObsidianVault().list_notes(exam_code):
        seed_certification_source_map(exam_code)

    context_query = query or " ".join(blueprint["focus_terms"])
    matches = StudyOpsRagIndex().query(
        query=context_query,
        certification=exam_code,
        top_k=5,
    )
    citation = matches[0]["citation"] if matches else ""
    count = _bounded_int(question_count, 1, 10)
    questions = []
    domains = list(blueprint["domains"])

    for index in range(count):
        topic = domains[index % len(domains)]
        questions.append(
            _make_question(
                exam_code=exam_code,
                topic=topic,
                question_index=index + 1,
                citation=citation,
            )
        )

    return {
        "certification": exam_code,
        "disclaimer": PRACTICE_DISCLAIMER,
        "question_count": len(questions),
        "questions": questions,
        "citations": [match["citation"] for match in matches],
        "retrieval_backend": matches[0]["backend"] if matches else "none",
    }


def submit_practice_answers(
    learner_id: str,
    certification: str,
    submitted_answers: list[dict[str, Any]],
) -> dict[str, Any]:
    """Score answers, store learner memory, and update retry queue."""

    ensure_storage_dirs()
    exam_code = get_exam_code(certification)
    if not submitted_answers:
        return {
            "certification": exam_code,
            "learner_id": learner_id,
            "score": 0.0,
            "attempt": None,
            "results": [],
            "memory": SQLiteStudyStore().get_progress_summary(learner_id, exam_code),
        }

    scored_answers = []
    correct_count = 0
    for answer in submitted_answers:
        selected = str(answer.get("selected_answer", "")).strip().upper()
        expected = str(answer.get("correct_answer", "")).strip().upper()
        correct = bool(answer.get("correct", False))
        if expected:
            correct = selected == expected
        if correct:
            correct_count += 1
        scored_answers.append(
            {
                "question_id": str(answer.get("question_id", "")),
                "selected_answer": selected,
                "correct_answer": expected,
                "correct": correct,
                "topic": str(answer.get("topic", "General")),
                "explanation": str(answer.get("explanation", "")),
            }
        )

    score = round((correct_count / len(scored_answers)) * 100, 2)
    store = SQLiteStudyStore()
    attempt = store.record_quiz_attempt(
        learner_id=learner_id,
        certification=exam_code,
        score=score,
        answers=scored_answers,
    )
    return {
        "certification": exam_code,
        "learner_id": learner_id,
        "score": score,
        "attempt": attempt.to_dict(),
        "results": scored_answers,
        "memory": store.get_progress_summary(learner_id, exam_code),
    }


def run_studyops_workflow(
    learner_id: str,
    certification: str,
    learner_goal: str = "",
    uploaded_file_paths: list[str] | None = None,
    hours_per_week: int = 5,
    question_count: int = 5,
) -> dict[str, Any]:
    """Run the focused MVP workflow from sources to quiz and memory."""

    ensure_storage_dirs()
    exam_code = get_exam_code(certification)
    blueprint = get_blueprint(exam_code)
    trace: list[WorkflowTraceStep] = []
    store = SQLiteStudyStore()
    store.ensure_learner(learner_id)

    source_map = seed_certification_source_map(exam_code)
    trace.append(
        WorkflowTraceStep(
            agent="Source Curator Agent",
            action="Selected official certification source candidates",
            output=f"{len(source_map['sources'])} source candidates for {exam_code}",
        )
    )

    allowed_sources = [
        source for source in source_map["sources"] if source.get("allowed", False)
    ]
    trace.append(
        WorkflowTraceStep(
            agent="Trust and Noise Filter Agent",
            action="Checked sources for trust, exam-dump language, and prompt injection",
            output=f"{len(allowed_sources)} sources allowed into the study workflow",
        )
    )

    ingested_files = []
    for file_path in uploaded_file_paths or []:
        ingested_files.append(
            ingest_study_file(
                certification=exam_code,
                file_path=str(Path(file_path)),
                title=Path(file_path).stem,
                domain="user_upload",
            )
        )
    trace.append(
        WorkflowTraceStep(
            agent="Knowledge Architect Agent",
            action="Created Obsidian notes and rebuilt the RAG index",
            output=(
                f"{1 + len(ingested_files)} notes/index updates prepared for "
                f"{blueprint['name']}"
            ),
        )
    )

    plan = create_study_plan(
        certification=exam_code,
        learner_goal=learner_goal,
        hours_per_week=hours_per_week,
    )
    trace.append(
        WorkflowTraceStep(
            agent="Study Planner Agent",
            action="Converted the blueprint into a weekly study plan",
            output=f"{len(plan['weekly_plan'])} blueprint domains planned",
        )
    )

    quiz = generate_practice_quiz(
        certification=exam_code,
        query=" ".join(blueprint["focus_terms"]),
        question_count=question_count,
    )
    trace.append(
        WorkflowTraceStep(
            agent="Practice Coach Agent",
            action="Generated safe exam-style practice questions",
            output=f"{quiz['question_count']} practice questions generated",
        )
    )

    memory = store.get_progress_summary(learner_id=learner_id, certification=exam_code)
    trace.append(
        WorkflowTraceStep(
            agent="Examiner and Remediation Agent",
            action="Loaded weak topics and retry queue",
            output=f"{len(memory['retry_queue'])} pending retry items",
        )
    )

    return {
        "workflow": "StudyOps focused MVP workflow",
        "certification": exam_code,
        "certification_name": blueprint["name"],
        "learner_id": learner_id,
        "trace": [step.to_dict() for step in trace],
        "source_map": source_map,
        "ingested_files": ingested_files,
        "study_plan": plan,
        "practice_quiz": quiz,
        "memory": memory,
    }
