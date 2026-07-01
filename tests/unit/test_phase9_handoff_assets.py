"""Contract checks for Phase 9 GitHub and Vercel handoff assets."""

from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Phase9HandoffAssetTests(unittest.TestCase):
    def test_phase9_files_exist(self) -> None:
        for relative_path in [
            "GITHUB_VERCEL_HANDOFF.md",
            "docs/phase-9-github-vercel-handoff.md",
            "scripts/preflight.ps1",
            "scripts/release-command-plan.ps1",
        ]:
            self.assertTrue((PROJECT_ROOT / relative_path).exists(), relative_path)

    def test_handoff_mentions_required_publish_targets(self) -> None:
        handoff = (PROJECT_ROOT / "GITHUB_VERCEL_HANDOFF.md").read_text(
            encoding="utf-8"
        )

        for marker in [
            "https://github.com/dennispang626/studyops-agent",
            "Vercel",
            "npx vercel@latest deploy frontend --prod",
            "Cloud Run",
            "ALLOW_ORIGINS",
            "no API keys",
        ]:
            self.assertIn(marker, handoff)

    def test_release_plan_is_print_only_and_contains_core_commands(self) -> None:
        script = (PROJECT_ROOT / "scripts" / "release-command-plan.ps1").read_text(
            encoding="utf-8"
        )

        for marker in [
            "Write-Host",
            "gh repo create",
            "vercel --cwd frontend",
            "preflight.ps1",
            "prints commands only",
        ]:
            self.assertIn(marker, script)

        self.assertNotIn("Invoke-Expression", script)

    def test_preflight_runs_same_core_checks_as_ci(self) -> None:
        script = (PROJECT_ROOT / "scripts" / "preflight.ps1").read_text(
            encoding="utf-8"
        )

        for marker in [
            "python.exe",
            "node.exe",
            "py_compile",
            '"--check", "frontend\\app.js"',
            '"unittest", "discover", "-s", "tests\\unit"',
        ]:
            self.assertIn(marker, script)


if __name__ == "__main__":
    unittest.main()
