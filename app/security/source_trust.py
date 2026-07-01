"""Source trust, exam-dump blocking, and redaction helpers."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from urllib.parse import urlparse


OFFICIAL_AWS_DOMAINS = {
    "aws.amazon.com",
    "docs.aws.amazon.com",
    "skillbuilder.aws",
    "explore.skillbuilder.aws",
}

TRUSTED_DOMAINS = {
    *OFFICIAL_AWS_DOMAINS,
    "github.com",
    "github.io",
}

EXAM_DUMP_PATTERNS = [
    "actual exam",
    "braindump",
    "brain dump",
    "dump",
    "exam dump",
    "free dumps",
    "guaranteed pass",
    "leaked",
    "pass guarantee",
    "real exam questions",
    "vce",
]

PROMPT_INJECTION_PATTERNS = [
    "developer message",
    "disregard all prior",
    "ignore all previous",
    "ignore previous instructions",
    "reveal your system prompt",
    "system prompt",
]

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[^\s,;]+"),
]

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_PATTERN = re.compile(r"\b(?:\+?\d[\d .-]{8,}\d)\b")


@dataclass(frozen=True)
class SourceTrustResult:
    """Trust classification for a source or snippet."""

    url: str
    domain: str
    trust_level: str
    allowed: bool
    reasons: list[str]
    flags: list[str]
    checked_at: str

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""

        return asdict(self)


def _domain_from_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.lower().removeprefix("www.")


def _contains_any(text: str, patterns: list[str]) -> list[str]:
    lower = text.lower()
    return [pattern for pattern in patterns if pattern in lower]


def classify_source(url: str, title: str = "", snippet: str = "") -> SourceTrustResult:
    """Classify whether a source is suitable for certification study."""

    domain = _domain_from_url(url)
    haystack = " ".join([url, title, snippet])
    reasons: list[str] = []
    flags: list[str] = []

    exam_dump_hits = _contains_any(haystack, EXAM_DUMP_PATTERNS)
    if exam_dump_hits:
        flags.append("exam_dump_language")
        reasons.append("Source appears to contain exam-dump or leaked-question language.")

    injection_hits = _contains_any(haystack, PROMPT_INJECTION_PATTERNS)
    if injection_hits:
        flags.append("prompt_injection_language")
        reasons.append("Source contains instruction-like text and must be treated as untrusted data.")

    if domain in OFFICIAL_AWS_DOMAINS:
        trust_level = "official"
        reasons.append("Official AWS source.")
    elif domain in TRUSTED_DOMAINS:
        trust_level = "trusted"
        reasons.append("Known trusted technical source.")
    elif not domain:
        trust_level = "unknown"
        reasons.append("Missing or invalid source URL.")
    else:
        trust_level = "unverified"
        reasons.append("Source is not in the trusted domain allowlist.")

    allowed = "exam_dump_language" not in flags and bool(domain)

    return SourceTrustResult(
        url=url,
        domain=domain,
        trust_level=trust_level,
        allowed=allowed,
        reasons=reasons,
        flags=flags,
        checked_at=datetime.now(UTC).isoformat(),
    )


def redact_sensitive_text(text: str) -> str:
    """Redact obvious secrets and PII before logging or storing text."""

    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED_SECRET]", redacted)
    redacted = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", redacted)
    redacted = PHONE_PATTERN.sub("[REDACTED_PHONE]", redacted)
    return redacted


def contains_prompt_injection(text: str) -> bool:
    """Return true when retrieved text contains instruction-like attack phrases."""

    return bool(_contains_any(text, PROMPT_INJECTION_PATTERNS))

