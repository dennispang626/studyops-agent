"""Chroma-compatible RAG index with a deterministic local fallback."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

from app.config import get_paths
from app.rag.chunking import RagChunk, chunks_from_vault


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+-]{1,}")


def tokenize(text: str) -> list[str]:
    """Tokenize text for the fallback retriever."""

    return [token.lower() for token in TOKEN_RE.findall(text)]


def _score(query_tokens: list[str], text: str) -> float:
    doc_tokens = Counter(tokenize(text))
    if not doc_tokens:
        return 0.0
    total = sum(doc_tokens.values())
    score = 0.0
    for token in query_tokens:
        if token in doc_tokens:
            score += 1.0 + math.log(1 + doc_tokens[token])
    return score / max(total, 1)


class StudyOpsRagIndex:
    """Index and query vault notes.

    Chroma is used when installed and enabled. Otherwise, a JSON fallback index
    gives deterministic local retrieval for tests and demos.
    """

    def __init__(self, index_dir: Path | None = None, collection_name: str = "studyops") -> None:
        self.paths = get_paths()
        self.index_dir = Path(index_dir or self.paths.chroma_dir)
        self.collection_name = collection_name
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.fallback_path = self.index_dir / "studyops_fallback_index.json"

    def _load_chroma(self):
        try:
            import chromadb  # type: ignore
        except ImportError:
            return None
        return chromadb

    def rebuild_from_vault(self, certification: str | None = None) -> dict[str, Any]:
        """Rebuild the index from Obsidian vault Markdown notes."""

        chunks = chunks_from_vault(certification)
        chromadb = self._load_chroma()
        if chromadb is not None:
            try:
                client = chromadb.PersistentClient(path=str(self.index_dir))
                collection = client.get_or_create_collection(self.collection_name)
                if chunks:
                    collection.upsert(
                        ids=[chunk.chunk_id for chunk in chunks],
                        documents=[chunk.text for chunk in chunks],
                        metadatas=[chunk.metadata for chunk in chunks],
                    )
                return {
                    "backend": "chroma",
                    "chunk_count": len(chunks),
                    "collection": self.collection_name,
                }
            except Exception as exc:  # pragma: no cover - dependency/runtime specific
                fallback = self._write_fallback(chunks)
                fallback["chroma_error"] = str(exc)
                return fallback

        return self._write_fallback(chunks)

    def _write_fallback(self, chunks: list[RagChunk]) -> dict[str, Any]:
        payload = {
            "backend": "json-fallback",
            "collection": self.collection_name,
            "chunks": [chunk.to_dict() for chunk in chunks],
        }
        self.fallback_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return {
            "backend": "json-fallback",
            "chunk_count": len(chunks),
            "path": str(self.fallback_path),
        }

    def query(
        self,
        query: str,
        certification: str | None = None,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """Retrieve relevant chunks with citation metadata."""

        chromadb = self._load_chroma()
        if chromadb is not None:
            try:
                client = chromadb.PersistentClient(path=str(self.index_dir))
                collection = client.get_or_create_collection(self.collection_name)
                where = {"certification": certification} if certification else None
                result = collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where=where,
                )
                documents = result.get("documents", [[]])[0]
                metadatas = result.get("metadatas", [[]])[0]
                distances = result.get("distances", [[]])[0]
                return [
                    {
                        "text": document,
                        "metadata": metadata,
                        "score": 1.0 / (1.0 + float(distance)),
                        "citation": metadata.get("path", ""),
                        "backend": "chroma",
                    }
                    for document, metadata, distance in zip(documents, metadatas, distances)
                ]
            except Exception:
                pass

        if not self.fallback_path.exists():
            self.rebuild_from_vault(certification)
        payload = json.loads(self.fallback_path.read_text(encoding="utf-8"))
        query_tokens = tokenize(query)
        matches = []
        for chunk in payload.get("chunks", []):
            metadata = chunk.get("metadata", {})
            if certification and metadata.get("certification") != certification:
                continue
            score = _score(query_tokens, chunk.get("text", ""))
            if score > 0:
                matches.append(
                    {
                        "text": chunk.get("text", ""),
                        "metadata": metadata,
                        "score": score,
                        "citation": metadata.get("path", ""),
                        "backend": payload.get("backend", "json-fallback"),
                    }
                )
        return sorted(matches, key=lambda item: item["score"], reverse=True)[:top_k]

