"""Static contract checks for the Phase 6 frontend."""

from __future__ import annotations

import unittest
from pathlib import Path


FRONTEND_ROOT = Path(__file__).resolve().parents[2] / "frontend"


class Phase6FrontendContractTests(unittest.TestCase):
    def test_frontend_files_exist(self) -> None:
        for filename in ["index.html", "styles.css", "app.js", "vercel.json"]:
            self.assertTrue((FRONTEND_ROOT / filename).exists(), filename)

    def test_index_exposes_required_app_regions(self) -> None:
        html = (FRONTEND_ROOT / "index.html").read_text(encoding="utf-8")

        for marker in [
            'id="homePage"',
            'id="setupPage"',
            'id="studyPage"',
            'id="practicePage"',
            'id="certificationSelect"',
            'id="saveSetupButton"',
            'id="setupStatus"',
            'id="apiBaseInput"',
            'id="apiBaseStatus"',
            'id="testApiBaseButton"',
            'id="runWorkflowButton"',
            'id="sourceList"',
            'id="domainList"',
            'id="activeStudyGuide"',
            'id="quizForm"',
            'id="weakTopicList"',
            'id="traceList"',
            "Generated exam-style practice, not official questions.",
        ]:
            self.assertIn(marker, html)

    def test_frontend_matches_backend_route_contract(self) -> None:
        javascript = (FRONTEND_ROOT / "app.js").read_text(encoding="utf-8")

        for marker in [
            "/api/studyops/workflow",
            "/api/studyops/health",
            "/api/studyops/rag-context",
            "/api/studyops/ingest-url",
            "/api/studyops/ingest-file",
            "/api/studyops/practice-submit",
            "studyops_api_base",
            "saveApiBase",
            "testApiBase",
            "clearApiBase",
            "contextItemFromBackendMatch",
            "studyops_memory:",
            "retryQueue",
            "buildPracticeQuiz",
            "classifySource",
            "studyops_session_settings",
            "saveSetup",
            "Unsaved changes",
            "option_explanations",
            "Correct is",
        ]:
            self.assertIn(marker, javascript)


if __name__ == "__main__":
    unittest.main()
