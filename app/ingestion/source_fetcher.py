"""Fetch and clean web sources for the StudyOps knowledge pipeline."""

from __future__ import annotations

import re
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser

from app.security.source_trust import (
    SourceTrustResult,
    classify_source,
    contains_prompt_injection,
    redact_sensitive_text,
)


WHITESPACE_RE = re.compile(r"\s+")


class TextHTMLParser(HTMLParser):
    """Small HTML-to-text parser that skips script/style content."""

    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._title_parts: list[str] = []
        self._text_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag in {"p", "br", "li", "h1", "h2", "h3", "h4"}:
            self._text_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self._title_parts.append(text)
        self._text_parts.append(text)

    @property
    def title(self) -> str:
        return WHITESPACE_RE.sub(" ", " ".join(self._title_parts)).strip()

    @property
    def text(self) -> str:
        text = "\n".join(self._text_parts)
        lines = [WHITESPACE_RE.sub(" ", line).strip() for line in text.splitlines()]
        return "\n".join(line for line in lines if line)


@dataclass(frozen=True)
class FetchedSource:
    """Cleaned source text and trust metadata."""

    url: str
    title: str
    text: str
    trust: SourceTrustResult
    fetched_at: str
    prompt_injection_detected: bool

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""

        data = asdict(self)
        data["trust"] = self.trust.to_dict()
        return data


def clean_html(html: str) -> tuple[str, str]:
    """Return `(title, clean_text)` from HTML."""

    parser = TextHTMLParser()
    parser.feed(html)
    return parser.title, redact_sensitive_text(parser.text)


def fetch_and_clean_url(
    url: str,
    title: str = "",
    snippet: str = "",
    timeout_seconds: int = 15,
    max_bytes: int = 1_500_000,
) -> FetchedSource:
    """Fetch a URL, clean HTML/text, and attach source-trust metadata."""

    initial_trust = classify_source(url=url, title=title, snippet=snippet)
    if not initial_trust.allowed:
        raise ValueError("; ".join(initial_trust.reasons))

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "StudyOpsAgent/0.1 "
                "(certification study assistant; respects source citations)"
            )
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            content_type = response.headers.get("Content-Type", "")
            raw = response.read(max_bytes)
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Unable to fetch source: {exc}") from exc

    decoded = raw.decode("utf-8", errors="replace")
    if "html" in content_type.lower() or "<html" in decoded.lower():
        parsed_title, clean_text = clean_html(decoded)
    else:
        parsed_title = title
        clean_text = redact_sensitive_text(decoded)

    final_title = title or parsed_title or url
    trust = classify_source(url=url, title=final_title, snippet=clean_text[:1000])
    if not trust.allowed:
        raise ValueError("; ".join(trust.reasons))

    return FetchedSource(
        url=url,
        title=final_title,
        text=clean_text,
        trust=trust,
        fetched_at=datetime.now(UTC).isoformat(),
        prompt_injection_detected=contains_prompt_injection(clean_text),
    )

