"""Markdown chunking for StudyOps RAG."""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from typing import Any

from app.storage.obsidian_vault import ObsidianVault


PARAGRAPH_SPLIT_RE = re.compile(r"\n{2,}")


@dataclass(frozen=True)
class RagChunk:
    """A retrievable text chunk with metadata."""

    chunk_id: str
    text: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary."""

        return asdict(self)


def _chunk_id(text: str, metadata: dict[str, Any]) -> str:
    source = f"{metadata.get('path', '')}:{metadata.get('chunk_index', '')}:{text}"
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:24]


def chunk_text(
    text: str,
    metadata: dict[str, Any],
    max_chars: int = 1200,
    overlap_chars: int = 160,
) -> list[RagChunk]:
    """Split Markdown text into overlapping chunks."""

    paragraphs = [part.strip() for part in PARAGRAPH_SPLIT_RE.split(text) if part.strip()]
    chunks: list[RagChunk] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunk_meta = {**metadata, "chunk_index": len(chunks)}
            chunks.append(RagChunk(_chunk_id(current, chunk_meta), current, chunk_meta))
            current = current[-overlap_chars:] + "\n\n" + paragraph
        else:
            current = paragraph[:max_chars]

    if current:
        chunk_meta = {**metadata, "chunk_index": len(chunks)}
        chunks.append(RagChunk(_chunk_id(current, chunk_meta), current, chunk_meta))
    return chunks


def chunks_from_vault(certification: str | None = None) -> list[RagChunk]:
    """Load Markdown notes from the Obsidian vault and split them into chunks."""

    vault = ObsidianVault()
    chunks: list[RagChunk] = []
    for note in vault.list_notes(certification):
        relative_path = note["path"]
        text = vault.read_note(relative_path)
        note_metadata = vault.get_note_metadata(relative_path)
        metadata = {
            "path": relative_path,
            "title": note_metadata.get("title") or note["title"],
            "certification": note_metadata.get("certification") or certification or "",
            "type": note_metadata.get("type", ""),
            "tags": note_metadata.get("tags", ""),
            "source_url": note_metadata.get("source_url", ""),
            "review_status": note_metadata.get("review_status", ""),
        }
        chunks.extend(chunk_text(text=text, metadata=metadata))
    return chunks
