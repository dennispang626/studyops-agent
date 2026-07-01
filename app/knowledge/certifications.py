"""Supported certification catalog and domain blueprints."""

from __future__ import annotations

from typing import Any


CERTIFICATION_CATALOG: dict[str, dict[str, Any]] = {
    "aws-ai-practitioner": {
        "name": "AWS Certified AI Practitioner",
        "exam_code": "AIF-C01",
        "official_sources": [
            "https://aws.amazon.com/certification/certified-ai-practitioner/",
            "https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html",
        ],
    },
    "aws-cloud-practitioner": {
        "name": "AWS Certified Cloud Practitioner",
        "exam_code": "CLF-C02",
        "official_sources": [
            "https://aws.amazon.com/certification/certified-cloud-practitioner/",
            "https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html",
        ],
    },
}

CERTIFICATION_ALIASES = {
    "aif-c01": "aws-ai-practitioner",
    "aws ai practitioner": "aws-ai-practitioner",
    "aws certified ai practitioner": "aws-ai-practitioner",
    "clf-c02": "aws-cloud-practitioner",
    "aws cloud practitioner": "aws-cloud-practitioner",
    "aws certified cloud practitioner": "aws-cloud-practitioner",
}

CERTIFICATION_BLUEPRINTS: dict[str, dict[str, Any]] = {
    "AIF-C01": {
        "name": "AWS Certified AI Practitioner",
        "domains": [
            "Fundamentals of AI and ML",
            "Fundamentals of generative AI",
            "Applications of foundation models",
            "Guidelines for responsible AI",
            "Security, compliance, and governance for AI solutions",
        ],
        "focus_terms": [
            "machine learning",
            "foundation models",
            "generative AI",
            "responsible AI",
            "security",
            "governance",
        ],
    },
    "CLF-C02": {
        "name": "AWS Certified Cloud Practitioner",
        "domains": [
            "Cloud concepts",
            "Security and compliance",
            "Cloud technology and services",
            "Billing, pricing, and support",
        ],
        "focus_terms": [
            "cloud value proposition",
            "shared responsibility",
            "AWS services",
            "billing",
            "support plans",
        ],
    },
}


def resolve_certification_key(certification: str) -> str:
    """Resolve a user-facing certification name/code to a catalog key."""

    normalized = certification.strip().lower()
    if normalized in CERTIFICATION_CATALOG:
        return normalized
    return CERTIFICATION_ALIASES.get(normalized, normalized)


def get_certification_item(certification: str) -> dict[str, Any] | None:
    """Return a catalog item by key, name, or exam code."""

    return CERTIFICATION_CATALOG.get(resolve_certification_key(certification))


def get_exam_code(certification: str) -> str:
    """Return the exam code when a certification is supported."""

    item = get_certification_item(certification)
    if item:
        return str(item["exam_code"])
    return certification


def get_blueprint(certification: str) -> dict[str, Any]:
    """Return a certification blueprint or a generic fallback."""

    exam_code = get_exam_code(certification)
    return CERTIFICATION_BLUEPRINTS.get(
        exam_code,
        {
            "name": certification,
            "domains": ["Core concepts", "Applied skills", "Review and practice"],
            "focus_terms": ["concepts", "skills", "practice"],
        },
    )

