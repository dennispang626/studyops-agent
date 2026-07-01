"""Load user-provided study files into the knowledge pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from app.security.source_trust import redact_sensitive_text


SUPPORTED_TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".html", ".htm"}


@dataclass(frozen=True)
class LoadedFile:
    """Loaded local file content."""

    path: str
    title: str
    text: str
    loaded_at: str

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""

        return asdict(self)


def load_study_file(file_path: str, title: str = "") -> LoadedFile:
    """Load a supported text-like study file.

    PDF parsing will be added later only if we install a PDF parser dependency.
    """

    path = Path(file_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Study file not found: {file_path}")

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        raise ValueError("PDF ingestion requires an optional parser and is not enabled yet.")
    if suffix not in SUPPORTED_TEXT_SUFFIXES:
        raise ValueError(f"Unsupported study file type: {suffix}")

    text = path.read_text(encoding="utf-8", errors="replace")
    return LoadedFile(
        path=str(path),
        title=title or path.stem.replace("-", " ").replace("_", " ").title(),
        text=redact_sensitive_text(text),
        loaded_at=datetime.now(UTC).isoformat(),
    )

