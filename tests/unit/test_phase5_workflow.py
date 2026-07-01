"""Deterministic tests for the Phase 5 multi-agent workflow."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from app.workflows.studyops_workflow import (
    create_study_plan,
    run_studyops_workflow,
    submit_practice_answers,
)


class Phase5WorkflowTests(unittest.TestCase):
    def test_study_plan_resolves_secondary_certification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            env = {
                "STUDYOPS_OBSIDIAN_VAULT": str(root / "vault"),
                "STUDYOPS_CHROMA_DIR": str(root / "chroma"),
                "STUDYOPS_SQLITE_PATH": str(root / "studyops.db"),
            }

            with mock.patch.dict("os.environ", env):
                plan = create_study_plan(
                    certification="AWS Cloud Practitioner",
                    learner_goal="Build baseline cloud confidence",
                    hours_per_week=4,
                )

        self.assertEqual(plan["certification"], "CLF-C02")
        self.assertEqual(len(plan["weekly_plan"]), 4)
        self.assertIn("retry", " ".join(plan["daily_loop"]).lower())

    def test_workflow_generates_trace_quiz_and_retry_memory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            env = {
                "STUDYOPS_OBSIDIAN_VAULT": str(root / "vault"),
                "STUDYOPS_CHROMA_DIR": str(root / "chroma"),
                "STUDYOPS_SQLITE_PATH": str(root / "studyops.db"),
            }

            with mock.patch.dict("os.environ", env):
                workflow = run_studyops_workflow(
                    learner_id="learner-1",
                    certification="AIF-C01",
                    learner_goal="Prepare for AWS AI Practitioner",
                    hours_per_week=5,
                    question_count=2,
                )
                questions = workflow["practice_quiz"]["questions"]
                wrong_answer = next(
                    option
                    for option in questions[0]["options"]
                    if option != questions[0]["correct_answer"]
                )
                scoring = submit_practice_answers(
                    learner_id="learner-1",
                    certification="AIF-C01",
                    submitted_answers=[
                        {
                            "question_id": questions[0]["question_id"],
                            "selected_answer": wrong_answer,
                            "correct_answer": questions[0]["correct_answer"],
                            "topic": questions[0]["topic"],
                            "explanation": questions[0]["explanation"],
                        },
                        {
                            "question_id": questions[1]["question_id"],
                            "selected_answer": questions[1]["correct_answer"],
                            "correct_answer": questions[1]["correct_answer"],
                            "topic": questions[1]["topic"],
                            "explanation": questions[1]["explanation"],
                        },
                    ],
                )

        trace_agents = [step["agent"] for step in workflow["trace"]]
        self.assertIn("Source Curator Agent", trace_agents)
        self.assertIn("Examiner and Remediation Agent", trace_agents)
        self.assertEqual(workflow["certification"], "AIF-C01")
        self.assertEqual(workflow["practice_quiz"]["question_count"], 2)
        self.assertIn("not official", workflow["practice_quiz"]["disclaimer"])
        self.assertEqual(scoring["score"], 50.0)
        self.assertEqual(len(scoring["memory"]["weak_topics"]), 2)
        self.assertEqual(len(scoring["memory"]["retry_queue"]), 1)


if __name__ == "__main__":
    unittest.main()
