"""Contract checks for Phase 7 eval and submission assets."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVAL_ROOT = PROJECT_ROOT / "tests" / "eval"
SUBMISSION_ROOT = PROJECT_ROOT / "submission"


class Phase7SubmissionAssetTests(unittest.TestCase):
    def test_eval_datasets_are_studyops_specific(self) -> None:
        for filename in [
            "basic-dataset.json",
            "studyops-capstone-dataset.json",
        ]:
            dataset_path = EVAL_ROOT / "datasets" / filename
            dataset = json.loads(dataset_path.read_text(encoding="utf-8"))

            self.assertIn("eval_cases", dataset)
            self.assertGreaterEqual(len(dataset["eval_cases"]), 4)
            serialized = json.dumps(dataset).lower()
            self.assertIn("studyops", serialized)
            self.assertIn("aws", serialized)
            self.assertNotIn("weather", serialized)

    def test_eval_config_contains_safety_and_trace_metrics(self) -> None:
        config = (EVAL_ROOT / "eval_config.yaml").read_text(encoding="utf-8")

        for marker in [
            "studyops_response_quality",
            "studyops_safety_static",
            "studyops_trace_completeness",
            "exam-dump",
            "generated questions as exam-style practice",
        ]:
            self.assertIn(marker, config)

    def test_submission_pack_files_exist(self) -> None:
        for filename in [
            "README.md",
            "kaggle-writeup-draft.md",
            "video-script.md",
            "demo-checklist.md",
            "architecture-for-writeup.md",
        ]:
            self.assertTrue((SUBMISSION_ROOT / filename).exists(), filename)

    def test_writeup_is_under_kaggle_word_limit_and_mentions_concepts(self) -> None:
        writeup = (SUBMISSION_ROOT / "kaggle-writeup-draft.md").read_text(
            encoding="utf-8"
        )
        words = re.findall(r"\b[\w'-]+\b", writeup)

        self.assertLessEqual(len(words), 2500)
        for marker in [
            "Agents for Good",
            "ADK",
            "MCP",
            "RAG",
            "Obsidian",
            "SQLite",
            "Generated exam-style practice",
        ]:
            self.assertIn(marker, writeup)


if __name__ == "__main__":
    unittest.main()

