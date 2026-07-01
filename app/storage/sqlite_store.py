"""SQLite learner memory and progress storage."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.config import get_paths


def utc_now() -> str:
    """Return an ISO timestamp in UTC."""

    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class QuizAttempt:
    """Quiz attempt summary."""

    id: int
    learner_id: str
    certification: str
    score: float
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary."""

        return asdict(self)


class SQLiteStudyStore:
    """Repository for learner progress, weak topics, sources, and retry queue."""

    def __init__(self, db_path: Path | str | None = None) -> None:
        self.db_path = Path(db_path or get_paths().sqlite_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self):
        """Open a SQLite connection with row dictionaries enabled."""

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        """Create storage tables when they do not exist."""

        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS learners (
                    id TEXT PRIMARY KEY,
                    display_name TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS quiz_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learner_id TEXT NOT NULL,
                    certification TEXT NOT NULL,
                    score REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (learner_id) REFERENCES learners(id)
                );

                CREATE TABLE IF NOT EXISTS answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    attempt_id INTEGER NOT NULL,
                    question_id TEXT NOT NULL,
                    selected_answer TEXT NOT NULL,
                    correct INTEGER NOT NULL,
                    topic TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    FOREIGN KEY (attempt_id) REFERENCES quiz_attempts(id)
                );

                CREATE TABLE IF NOT EXISTS weak_topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learner_id TEXT NOT NULL,
                    certification TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    misses INTEGER NOT NULL DEFAULT 0,
                    last_seen_at TEXT NOT NULL,
                    mastery_score REAL NOT NULL DEFAULT 0,
                    UNIQUE (learner_id, certification, topic)
                );

                CREATE TABLE IF NOT EXISTS retry_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learner_id TEXT NOT NULL,
                    certification TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    due_at TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending'
                );

                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    certification TEXT NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    trust_level TEXT NOT NULL,
                    retrieved_at TEXT NOT NULL,
                    UNIQUE (certification, url)
                );
                """
            )

    def ensure_learner(self, learner_id: str, display_name: str | None = None) -> None:
        """Create a learner row if needed."""

        with self.connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO learners (id, display_name, created_at)
                VALUES (?, ?, ?)
                """,
                (learner_id, display_name or learner_id, utc_now()),
            )

    def record_source(
        self, certification: str, url: str, title: str, trust_level: str
    ) -> dict[str, Any]:
        """Insert or update a certification source record."""

        retrieved_at = utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO sources (certification, url, title, trust_level, retrieved_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(certification, url) DO UPDATE SET
                    title = excluded.title,
                    trust_level = excluded.trust_level,
                    retrieved_at = excluded.retrieved_at
                """,
                (certification, url, title, trust_level, retrieved_at),
            )
            row = conn.execute(
                "SELECT * FROM sources WHERE certification = ? AND url = ?",
                (certification, url),
            ).fetchone()
        return dict(row)

    def record_quiz_attempt(
        self,
        learner_id: str,
        certification: str,
        score: float,
        answers: list[dict[str, Any]],
    ) -> QuizAttempt:
        """Record a quiz attempt and update weak-topic memory."""

        self.ensure_learner(learner_id)
        created_at = utc_now()
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO quiz_attempts (learner_id, certification, score, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (learner_id, certification, score, created_at),
            )
            attempt_id = int(cursor.lastrowid)

            for answer in answers:
                correct = bool(answer.get("correct", False))
                topic = str(answer.get("topic", "General"))
                conn.execute(
                    """
                    INSERT INTO answers
                    (attempt_id, question_id, selected_answer, correct, topic, explanation)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        attempt_id,
                        str(answer.get("question_id", "")),
                        str(answer.get("selected_answer", "")),
                        1 if correct else 0,
                        topic,
                        str(answer.get("explanation", "")),
                    ),
                )
                self._update_weak_topic(
                    conn=conn,
                    learner_id=learner_id,
                    certification=certification,
                    topic=topic,
                    correct=correct,
                )

        return QuizAttempt(
            id=attempt_id,
            learner_id=learner_id,
            certification=certification,
            score=score,
            created_at=created_at,
        )

    def _update_weak_topic(
        self,
        conn: sqlite3.Connection,
        learner_id: str,
        certification: str,
        topic: str,
        correct: bool,
    ) -> None:
        last_seen_at = utc_now()
        existing = conn.execute(
            """
            SELECT * FROM weak_topics
            WHERE learner_id = ? AND certification = ? AND topic = ?
            """,
            (learner_id, certification, topic),
        ).fetchone()

        if existing is None:
            misses = 0 if correct else 1
            mastery_score = 0.75 if correct else 0.0
            conn.execute(
                """
                INSERT INTO weak_topics
                (learner_id, certification, topic, misses, last_seen_at, mastery_score)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (learner_id, certification, topic, misses, last_seen_at, mastery_score),
            )
        else:
            misses = int(existing["misses"]) + (0 if correct else 1)
            mastery_score = min(1.0, float(existing["mastery_score"]) + 0.15)
            if not correct:
                mastery_score = max(0.0, mastery_score - 0.35)
            conn.execute(
                """
                UPDATE weak_topics
                SET misses = ?, last_seen_at = ?, mastery_score = ?
                WHERE learner_id = ? AND certification = ? AND topic = ?
                """,
                (
                    misses,
                    last_seen_at,
                    mastery_score,
                    learner_id,
                    certification,
                    topic,
                ),
            )

        if not correct:
            conn.execute(
                """
                INSERT INTO retry_queue (learner_id, certification, topic, due_at, status)
                VALUES (?, ?, ?, ?, 'pending')
                """,
                (learner_id, certification, topic, last_seen_at),
            )

    def get_weak_topics(
        self, learner_id: str, certification: str | None = None
    ) -> list[dict[str, Any]]:
        """Return weak topics ordered by misses and recency."""

        with self.connect() as conn:
            if certification:
                rows = conn.execute(
                    """
                    SELECT * FROM weak_topics
                    WHERE learner_id = ? AND certification = ?
                    ORDER BY misses DESC, last_seen_at DESC
                    """,
                    (learner_id, certification),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT * FROM weak_topics
                    WHERE learner_id = ?
                    ORDER BY misses DESC, last_seen_at DESC
                    """,
                    (learner_id,),
                ).fetchall()
        return [dict(row) for row in rows]

    def get_retry_queue(
        self, learner_id: str, certification: str | None = None
    ) -> list[dict[str, Any]]:
        """Return pending retry queue items."""

        with self.connect() as conn:
            if certification:
                rows = conn.execute(
                    """
                    SELECT * FROM retry_queue
                    WHERE learner_id = ? AND certification = ? AND status = 'pending'
                    ORDER BY due_at ASC
                    """,
                    (learner_id, certification),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT * FROM retry_queue
                    WHERE learner_id = ? AND status = 'pending'
                    ORDER BY due_at ASC
                    """,
                    (learner_id,),
                ).fetchall()
        return [dict(row) for row in rows]

    def get_progress_summary(
        self, learner_id: str, certification: str
    ) -> dict[str, Any]:
        """Return score history, weak topics, and retry queue for one learner."""

        with self.connect() as conn:
            attempts = conn.execute(
                """
                SELECT * FROM quiz_attempts
                WHERE learner_id = ? AND certification = ?
                ORDER BY created_at DESC
                """,
                (learner_id, certification),
            ).fetchall()
        return {
            "learner_id": learner_id,
            "certification": certification,
            "attempts": [dict(row) for row in attempts],
            "weak_topics": self.get_weak_topics(learner_id, certification),
            "retry_queue": self.get_retry_queue(learner_id, certification),
        }
