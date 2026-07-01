"""Obsidian-compatible Markdown vault operations."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.config import get_paths
from app.security.source_trust import redact_sensitive_text


SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class NoteRecord:
    """Metadata for a Markdown note in the Obsidian vault."""

    certification: str
    title: str
    path: str
    source_url: str | None
    created_at: str

    def to_dict(self) -> dict[str, str | None]:
        """Return a JSON-serializable dictionary."""

        return asdict(self)


def slugify(value: str) -> str:
    """Create a filesystem-safe lowercase slug."""

    slug = SLUG_PATTERN.sub("-", value.lower()).strip("-")
    return slug or "untitled"


class ObsidianVault:
    """Small Markdown vault wrapper used before the RAG index is built."""

    def __init__(self, vault_root: Path | None = None) -> None:
        self.vault_root = Path(vault_root or get_paths().obsidian_vault).resolve()
        self.vault_root.mkdir(parents=True, exist_ok=True)

    def _certification_dir(self, certification: str) -> Path:
        path = self.vault_root / certification
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _safe_note_path(self, certification: str, title: str) -> Path:
        note_path = self._certification_dir(certification) / f"{slugify(title)}.md"
        resolved = note_path.resolve()
        if not str(resolved).startswith(str(self.vault_root)):
            raise ValueError("Resolved note path escapes the Obsidian vault.")
        return resolved

    def write_note(
        self,
        certification: str,
        title: str,
        body: str,
        source_url: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> NoteRecord:
        """Write a Markdown note with simple front matter."""

        created_at = datetime.now(UTC).isoformat()
        clean_body = redact_sensitive_text(body)
        front_matter = {
            "certification": certification,
            "title": title,
            "source_url": source_url or "",
            "created_at": created_at,
            **(metadata or {}),
        }
        front_matter_text = "\n".join(
            f"{key}: {str(value).replace(chr(10), ' ')}"
            for key, value in front_matter.items()
        )
        content = f"---\n{front_matter_text}\n---\n\n# {title}\n\n{clean_body}\n"
        note_path = self._safe_note_path(certification, title)
        note_path.write_text(content, encoding="utf-8")
        return NoteRecord(
            certification=certification,
            title=title,
            path=str(note_path.relative_to(self.vault_root)),
            source_url=source_url,
            created_at=created_at,
        )

    def read_note(self, relative_path: str) -> str:
        """Read a note by a vault-relative path."""

        note_path = (self.vault_root / relative_path).resolve()
        if not str(note_path).startswith(str(self.vault_root)):
            raise ValueError("Requested note path escapes the Obsidian vault.")
        return note_path.read_text(encoding="utf-8")

    def list_notes(self, certification: str | None = None) -> list[dict[str, str]]:
        """List Markdown notes in the vault."""

        root = self._certification_dir(certification) if certification else self.vault_root
        notes = []
        for path in sorted(root.rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            notes.append(
                {
                    "path": str(path.relative_to(self.vault_root)),
                    "title": path.stem.replace("-", " ").title(),
                }
            )
        return notes

    def search_notes(self, query: str, certification: str | None = None) -> list[dict[str, str]]:
        """Perform a simple keyword search over Markdown notes.

        This is a lightweight pre-RAG search. Chroma semantic retrieval arrives
        in Phase 4.
        """

        query_terms = {term.lower() for term in re.findall(r"[a-zA-Z0-9]+", query)}
        if not query_terms:
            return []

        matches = []
        for note in self.list_notes(certification):
            content = self.read_note(note["path"])
            lower = content.lower()
            score = sum(1 for term in query_terms if term in lower)
            if score:
                matches.append({**note, "score": str(score)})
        return sorted(matches, key=lambda item: int(item["score"]), reverse=True)

