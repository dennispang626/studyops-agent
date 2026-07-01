"""Local configuration helpers for StudyOps Agent."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class StudyOpsPaths:
    """Filesystem paths used by the local-first prototype."""

    project_root: Path
    obsidian_vault: Path
    chroma_dir: Path
    sqlite_path: Path


def _path_from_env(name: str, default: str) -> Path:
    raw = os.getenv(name, default)
    path = Path(raw)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def get_paths() -> StudyOpsPaths:
    """Return normalized StudyOps storage paths."""

    return StudyOpsPaths(
        project_root=PROJECT_ROOT,
        obsidian_vault=_path_from_env(
            "STUDYOPS_OBSIDIAN_VAULT", "data/obsidian_vault"
        ),
        chroma_dir=_path_from_env("STUDYOPS_CHROMA_DIR", "data/chroma"),
        sqlite_path=_path_from_env("STUDYOPS_SQLITE_PATH", "data/sqlite/studyops.db"),
    )


def ensure_storage_dirs(paths: StudyOpsPaths | None = None) -> StudyOpsPaths:
    """Create local storage folders and return the active path config."""

    active_paths = paths or get_paths()
    active_paths.obsidian_vault.mkdir(parents=True, exist_ok=True)
    active_paths.chroma_dir.mkdir(parents=True, exist_ok=True)
    active_paths.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    return active_paths

