"""Obsidian-compatible Markdown vault operations."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.config import get_paths
from app.knowledge.certifications import get_blueprint, get_certification_slug, get_exam_code
from app.security.source_trust import redact_sensitive_text


SLUG_PATTERN = re.compile(r"[^a-z0-9]+")
FRONT_MATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)


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
    """OKF-style Markdown vault wrapper used by the long-term memory layer."""

    def __init__(self, vault_root: Path | None = None) -> None:
        self.vault_root = Path(vault_root or get_paths().obsidian_vault).resolve()
        self.vault_root.mkdir(parents=True, exist_ok=True)
        (self.vault_root / ".obsidian").mkdir(exist_ok=True)

    def _safe_relative_path(self, relative_path: str | Path) -> Path:
        note_path = (self.vault_root / relative_path).resolve()
        if not str(note_path).startswith(str(self.vault_root)):
            raise ValueError("Resolved note path escapes the Obsidian vault.")
        return note_path

    def _ensure_dir(self, relative_path: str | Path) -> Path:
        path = self._safe_relative_path(relative_path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _certification_dir(self, certification: str) -> Path:
        return self._ensure_dir(Path("certificates") / get_certification_slug(certification))

    def _safe_note_path(self, relative_dir: str | Path, slug: str) -> Path:
        return self._safe_relative_path(Path(relative_dir) / f"{slugify(slug)}.md")

    def _relative_note_path(self, relative_dir: str | Path, slug: str) -> str:
        return str(Path(relative_dir) / f"{slugify(slug)}.md")

    def _yaml_value(self, value: Any) -> str:
        if isinstance(value, list):
            return "[" + ", ".join(str(item).replace('"', "'") for item in value) + "]"
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value).replace("\n", " ").replace('"', "'")

    def _front_matter(self, metadata: dict[str, Any]) -> str:
        return "\n".join(
            f"{key}: {self._yaml_value(value)}"
            for key, value in metadata.items()
            if value is not None
        )

    def _write_raw_note(
        self,
        relative_path: str | Path,
        title: str,
        body: str,
        metadata: dict[str, Any],
    ) -> NoteRecord:
        created_at = str(metadata.get("created", datetime.now(UTC).isoformat()))
        clean_body = redact_sensitive_text(body)
        note_path = self._safe_relative_path(relative_path)
        note_path.parent.mkdir(parents=True, exist_ok=True)
        content = (
            f"---\n{self._front_matter(metadata)}\n---\n\n"
            f"# {title}\n\n{clean_body.strip()}\n"
        )
        note_path.write_text(content, encoding="utf-8")
        return NoteRecord(
            certification=str(metadata.get("certification", "")),
            title=title,
            path=note_path.relative_to(self.vault_root).as_posix(),
            source_url=str(metadata.get("source_url", "")) or None,
            created_at=created_at,
        )

    def write_okf_note(
        self,
        *,
        note_type: str,
        title: str,
        body: str,
        relative_path: str | Path,
        certification: str = "",
        description: str = "",
        tags: list[str] | None = None,
        source_url: str | None = None,
        source_ids: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> NoteRecord:
        """Write an OKF-style Markdown note with portable front matter."""

        now = datetime.now(UTC).isoformat()
        exam_code = get_exam_code(certification) if certification else ""
        front_matter = {
            "type": note_type,
            "title": title,
            "description": description,
            "tags": tags or [],
            "certification": exam_code,
            "provider": "AWS" if exam_code in {"AIF-C01", "CLF-C02"} else "",
            "source_url": source_url or "",
            "source_ids": source_ids or [],
            "review_status": "agent_drafted",
            "format": "okf-style-markdown",
            "format_version": "0.1",
            "created": now,
            "updated": now,
            **(metadata or {}),
        }
        return self._write_raw_note(
            relative_path=relative_path,
            title=title,
            body=body,
            metadata=front_matter,
        )

    def ensure_okf_structure(self, certification: str) -> dict[str, Any]:
        """Create the recommended OKF-style vault skeleton for a certification."""

        exam_code = get_exam_code(certification)
        cert_slug = get_certification_slug(exam_code)
        blueprint = get_blueprint(exam_code)

        for folder in [
            "certificates",
            Path("certificates") / cert_slug,
            "concepts",
            "sources",
            "quizzes",
        ]:
            self._ensure_dir(folder)

        root_index = self.write_okf_note(
            note_type="index",
            title="StudyOps Knowledge Base",
            description="Agent-maintained certification study wiki.",
            relative_path="index.md",
            tags=["studyops", "knowledge-base", "rag"],
            body=(
                "StudyOps keeps raw sources separate from the curated wiki.\n\n"
                "## Main Areas\n\n"
                f"- [[certificates/{cert_slug}/index|{blueprint['name']}]]\n"
                "- [[concepts]]\n"
                "- [[sources]]\n"
                "- [[quizzes/weak-topics|Weak topics]]\n"
            ),
            metadata={"certification": exam_code},
        )

        cert_index = self.write_okf_note(
            note_type="certificate",
            title=blueprint["name"],
            description=f"Study hub for {blueprint['name']} ({exam_code}).",
            relative_path=Path("certificates") / cert_slug / "index.md",
            certification=exam_code,
            tags=["certificate", cert_slug, exam_code.lower()],
            body=(
                f"Exam code: {exam_code}\n\n"
                "## Study Pages\n\n"
                "- [[exam-blueprint]]\n"
                "- [[study-plan]]\n\n"
                "## Source and Concept Memory\n\n"
                "- [[../../sources]]\n"
                "- [[../../concepts]]\n"
                "- [[../../quizzes/weak-topics|Weak topics]]\n"
            ),
        )

        blueprint_note = self.write_exam_blueprint(
            certification=exam_code,
            official_sources=[],
        )
        study_plan_note = self.write_okf_note(
            note_type="study_plan",
            title=f"{blueprint['name']} Study Plan",
            description="Reusable study loop for certification preparation.",
            relative_path=Path("certificates") / cert_slug / "study-plan.md",
            certification=exam_code,
            tags=["study-plan", cert_slug],
            body=(
                "## Study Loop\n\n"
                "1. Add or refresh trusted sources.\n"
                "2. Let the agent compile notes into the OKF-style wiki.\n"
                "3. Retrieve cited context from the Chroma index.\n"
                "4. Practice generated exam-style questions.\n"
                "5. Move misses into [[../../quizzes/weak-topics|weak topics]].\n"
            ),
        )
        weak_topics_note = self.write_okf_note(
            note_type="quiz_memory",
            title="Weak Topics",
            description="Learner remediation queue and review notes.",
            relative_path=Path("quizzes") / "weak-topics.md",
            certification=exam_code,
            tags=["quiz", "remediation", "memory"],
            body=(
                "Weak topics are updated from SQLite learner memory and can be "
                "reviewed here by humans.\n"
            ),
        )

        concept_names = list(dict.fromkeys([*blueprint["domains"], *blueprint["focus_terms"]]))
        concept_notes = [
            self.write_concept_note(certification=exam_code, concept=concept)
            for concept in concept_names
        ]
        return {
            "root_index": root_index.to_dict(),
            "certificate_index": cert_index.to_dict(),
            "exam_blueprint": blueprint_note.to_dict(),
            "study_plan": study_plan_note.to_dict(),
            "weak_topics": weak_topics_note.to_dict(),
            "concepts": [note.to_dict() for note in concept_notes],
        }

    def write_exam_blueprint(
        self,
        certification: str,
        official_sources: list[str] | None = None,
    ) -> NoteRecord:
        """Write the certificate exam blueprint note in the OKF structure."""

        exam_code = get_exam_code(certification)
        cert_slug = get_certification_slug(exam_code)
        blueprint = get_blueprint(exam_code)
        domain_lines = "\n".join(
            f"- [[../../concepts/{slugify(domain)}|{domain}]]"
            for domain in blueprint["domains"]
        )
        focus_lines = "\n".join(
            f"- [[../../concepts/{slugify(term)}|{term}]]"
            for term in blueprint["focus_terms"]
        )
        source_lines = "\n".join(f"- {url}" for url in official_sources or [])
        if not source_lines:
            source_lines = "- Source candidates are added during ingestion."
        return self.write_okf_note(
            note_type="exam_blueprint",
            title=f"{blueprint['name']} Exam Blueprint",
            description=f"Blueprint domains and retrieval focus for {exam_code}.",
            relative_path=Path("certificates") / cert_slug / "exam-blueprint.md",
            certification=exam_code,
            tags=["exam-blueprint", cert_slug, exam_code.lower()],
            source_ids=[slugify(url) for url in official_sources or []],
            body=(
                "## Exam Domains\n\n"
                f"{domain_lines}\n\n"
                "## Retrieval Focus Terms\n\n"
                f"{focus_lines}\n\n"
                "## Official Source Candidates\n\n"
                f"{source_lines}\n"
            ),
        )

    def write_concept_note(
        self,
        certification: str,
        concept: str,
        body: str = "",
        source_ids: list[str] | None = None,
    ) -> NoteRecord:
        """Write or refresh a concept page linked from certificate notes."""

        exam_code = get_exam_code(certification)
        cert_slug = get_certification_slug(exam_code)
        concept_slug = slugify(concept)
        content = body or (
            f"This concept is part of [[../certificates/{cert_slug}/index|{exam_code}]] study memory.\n\n"
            "## Review Prompts\n\n"
            f"- Explain {concept} in your own words.\n"
            f"- Connect {concept} to at least one workplace scenario.\n"
            "- Verify claims against cited source notes before using them in quiz feedback.\n"
        )
        return self.write_okf_note(
            note_type="concept",
            title=concept.title(),
            description=f"Study concept for {exam_code}.",
            relative_path=Path("concepts") / f"{concept_slug}.md",
            certification=exam_code,
            tags=["concept", cert_slug, concept_slug],
            source_ids=source_ids or [],
            body=content,
        )

    def write_source_note(
        self,
        certification: str,
        title: str,
        body: str,
        source_url: str = "",
        domain: str = "",
        trust_level: str = "",
        source_kind: str = "source",
        metadata: dict[str, Any] | None = None,
    ) -> NoteRecord:
        """Write a source-derived note under `sources/`."""

        exam_code = get_exam_code(certification)
        cert_slug = get_certification_slug(exam_code)
        note_slug = slugify(title)
        return self.write_okf_note(
            note_type=source_kind,
            title=title,
            description=f"Curated source note for {exam_code}.",
            relative_path=Path("sources") / f"{note_slug}.md",
            certification=exam_code,
            tags=["source", cert_slug, slugify(domain or trust_level or "study")],
            source_url=source_url,
            source_ids=[note_slug],
            metadata={"domain": domain, "trust_level": trust_level, **(metadata or {})},
            body=body,
        )

    def write_note(
        self,
        certification: str,
        title: str,
        body: str,
        source_url: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> NoteRecord:
        """Write a source note with OKF-style front matter.

        This keeps the original public method while routing new content into the
        OKF-style `sources/` directory instead of legacy exam-code folders.
        """

        meta = metadata or {}
        return self.write_source_note(
            certification=certification,
            title=title,
            body=body,
            source_url=source_url or "",
            domain=str(meta.get("domain", "")),
            trust_level=str(meta.get("trust_level", "")),
            source_kind=str(meta.get("type", "source")),
            metadata=meta,
        )

    def read_note(self, relative_path: str) -> str:
        """Read a note by a vault-relative path."""

        note_path = self._safe_relative_path(relative_path)
        return note_path.read_text(encoding="utf-8")

    def get_note_metadata(self, relative_path: str) -> dict[str, str]:
        """Return parsed front matter metadata for a note."""

        text = self.read_note(relative_path)
        match = FRONT_MATTER_RE.match(text)
        if not match:
            return {}
        metadata = {}
        for line in match.group("body").splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"')
        return metadata

    def list_notes(self, certification: str | None = None) -> list[dict[str, str]]:
        """List Markdown notes in the vault."""

        exam_code = get_exam_code(certification) if certification else ""
        notes = []
        for path in sorted(self.vault_root.rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            relative_path = path.relative_to(self.vault_root).as_posix()
            metadata = self.get_note_metadata(relative_path)
            if exam_code and metadata.get("certification") != exam_code:
                continue
            notes.append(
                {
                    "path": relative_path,
                    "title": metadata.get("title") or path.stem.replace("-", " ").title(),
                    "type": metadata.get("type", ""),
                    "certification": metadata.get("certification", ""),
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
