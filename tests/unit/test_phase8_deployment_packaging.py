"""Contract checks for Phase 8 deployment packaging."""

from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Phase8DeploymentPackagingTests(unittest.TestCase):
    def test_deployment_files_exist(self) -> None:
        for relative_path in [
            "DEPLOYMENT.md",
            ".dockerignore",
            ".github/workflows/ci.yml",
            "frontend/package.json",
            "docs/phase-8-deployment-packaging.md",
            ".env.example",
            ".gitignore",
        ]:
            self.assertTrue((PROJECT_ROOT / relative_path).exists(), relative_path)

    def test_dockerfile_does_not_require_missing_lockfile(self) -> None:
        dockerfile = (PROJECT_ROOT / "Dockerfile").read_text(encoding="utf-8")

        self.assertIn("uv sync --no-dev", dockerfile)
        self.assertNotIn("uv.lock*", dockerfile)
        self.assertNotIn("--frozen", dockerfile)

    def test_ci_runs_core_checks(self) -> None:
        ci = (PROJECT_ROOT / ".github" / "workflows" / "ci.yml").read_text(
            encoding="utf-8"
        )

        for marker in [
            "python -m py_compile",
            "node --check frontend/app.js",
            "python -m unittest discover -s tests/unit",
        ]:
            self.assertIn(marker, ci)

    def test_deployment_guide_mentions_required_targets(self) -> None:
        guide = (PROJECT_ROOT / "DEPLOYMENT.md").read_text(encoding="utf-8")

        for marker in [
            "Vercel",
            "Cloud Run",
            "GitHub",
            "ALLOW_ORIGINS",
            "agents-cli eval generate",
        ]:
            self.assertIn(marker, guide)


if __name__ == "__main__":
    unittest.main()

