"""Contract checks for the personal local backend bridge."""

from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class LocalBackendBridgeContractTests(unittest.TestCase):
    def test_health_endpoint_reports_pipeline_readiness(self) -> None:
        backend = (PROJECT_ROOT / "app" / "fast_api_app.py").read_text(
            encoding="utf-8"
        )

        for marker in [
            '@app.get("/api/studyops/health")',
            "studyops-local-bridge",
            "gemini_api_key_configured",
            "vault_notes",
            "rag_index_ready",
            "sqlite_ready",
            "/api/studyops/ingest-url",
            "/api/studyops/ingest-file",
        ]:
            self.assertIn(marker, backend)

    def test_local_backend_launcher_loads_ignored_env_files(self) -> None:
        script = (PROJECT_ROOT / "scripts" / "start-local-backend.ps1").read_text(
            encoding="utf-8"
        )

        for marker in [
            'Import-DotEnv ".env"',
            'Import-DotEnv ".env.local"',
            "studyops-agent.vercel.app",
            "GOOGLE_API_KEY configured",
            "uvicorn app.fast_api_app:app",
        ]:
            self.assertIn(marker, script)


if __name__ == "__main__":
    unittest.main()
