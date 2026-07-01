"""Deterministic tests for Phase 3 storage and safety foundations."""

from __future__ import annotations

import tempfile
import unittest
from unittest import mock
from pathlib import Path

from app.security.source_trust import classify_source, redact_sensitive_text
from app.storage.obsidian_vault import ObsidianVault
from app.storage.sqlite_store import SQLiteStudyStore
from app.tools.studyops_tools import search_certification_sources


class SourceTrustTests(unittest.TestCase):
    def test_official_aws_source_is_allowed(self) -> None:
        result = classify_source(
            "https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html"
        )

        self.assertTrue(result.allowed)
        self.assertEqual(result.trust_level, "official")

    def test_exam_dump_source_is_blocked(self) -> None:
        result = classify_source(
            "https://example.com/aws-aif-c01-dumps",
            title="Real exam questions and answers",
        )

        self.assertFalse(result.allowed)
        self.assertIn("exam_dump_language", result.flags)

    def test_redaction_removes_email_and_secret(self) -> None:
        secret_name = "api" + "_key"
        text = f"Email me at user@example.com {secret_name}=abcdef123456"

        redacted = redact_sensitive_text(text)

        self.assertIn("[REDACTED_EMAIL]", redacted)
        self.assertIn("[REDACTED_SECRET]", redacted)


class ObsidianVaultTests(unittest.TestCase):
    def test_write_and_list_note(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            vault = ObsidianVault(Path(tmp_dir))
            note = vault.write_note(
                certification="AWS AI Practitioner",
                title="Exam Overview",
                body="AIF-C01 validates AI, ML, and generative AI fundamentals.",
                source_url="https://aws.amazon.com/certification/certified-ai-practitioner/",
            )

            notes = vault.list_notes("AWS AI Practitioner")

            self.assertEqual(
                note.path, str(Path("AWS AI Practitioner") / "exam-overview.md")
            )
            self.assertEqual(len(notes), 1)
            self.assertIn("Exam Overview", vault.read_note(note.path))


class ToolFoundationTests(unittest.TestCase):
    def test_curated_source_search_returns_official_aif_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = str(Path(tmp_dir) / "studyops.db")
            with mock.patch.dict("os.environ", {"STUDYOPS_SQLITE_PATH": db_path}):
                sources = search_certification_sources("AIF-C01")

            self.assertEqual(len(sources), 2)
            self.assertTrue(
                all(source["trust"]["trust_level"] == "official" for source in sources)
            )


class SQLiteStoreTests(unittest.TestCase):
    def test_record_attempt_updates_retry_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            store = SQLiteStudyStore(Path(tmp_dir) / "studyops.db")
            attempt = store.record_quiz_attempt(
                learner_id="learner-1",
                certification="AIF-C01",
                score=50,
                answers=[
                    {
                        "question_id": "q1",
                        "selected_answer": "B",
                        "correct": False,
                        "topic": "Responsible AI",
                        "explanation": "Review fairness and transparency.",
                    }
                ],
            )

            summary = store.get_progress_summary("learner-1", "AIF-C01")

            self.assertEqual(attempt.learner_id, "learner-1")
            self.assertEqual(len(summary["weak_topics"]), 1)
            self.assertEqual(len(summary["retry_queue"]), 1)
            self.assertEqual(summary["weak_topics"][0]["topic"], "Responsible AI")


if __name__ == "__main__":
    unittest.main()
