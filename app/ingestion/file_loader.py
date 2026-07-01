"""Load user-provided study files into the knowledge pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from app.security.source_trust import redact_sensitive_text


SUPPORTED_TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".html", ".htm"}
SUPPORTED_SUFFIXES = {*SUPPORTED_TEXT_SUFFIXES, ".pdf"}


def _load_pdf_text(path: Path) -> str:
    """Extract text from a PDF when the optional parser is installed."""

    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError as exc:  # pragma: no cover - optional dependency path
        raise ValueError(
            "PDF ingestion requires pypdf. Install project dependencies with `uv sync`."
        ) from exc

    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n\n".join(page.strip() for page in pages if page.strip())


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

    PDFs use the optional pypdf parser so raw uploads can enter the same
    Markdown-wiki and RAG pipeline as text sources.
    """

    path = Path(file_path).expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Study file not found: {file_path}")

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text = _load_pdf_text(path)
        return LoadedFile(
            path=str(path),
            title=title or path.stem.replace("-", " ").replace("_", " ").title(),
            text=redact_sensitive_text(text),
            loaded_at=datetime.now(UTC).isoformat(),
        )
    if suffix not in SUPPORTED_TEXT_SUFFIXES:
        raise ValueError(f"Unsupported study file type: {suffix}")

    text = path.read_text(encoding="utf-8", errors="replace")
    return LoadedFile(
        path=str(path),
        title=title or path.stem.replace("-", " ").replace("_", " ").title(),
        text=redact_sensitive_text(text),
        loaded_at=datetime.now(UTC).isoformat(),
    )
